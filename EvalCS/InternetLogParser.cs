using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace EvalCS
{
    class InternetLogParser
    {
        public class Datapoint
        {
            public Datapoint(string time, List<TestColumn> testColumns)
            {
                Time = time;
                TestColumns = testColumns;
            }

            public string Time { get; }
            public List<TestColumn> TestColumns { get; }
        }


        public class TestColumn
        {
            public TestColumn(string name, string value)
            {
                Name = name;
                Value = value;
            }
            public string Name { get; }
            public string Value { get; }
        }



        public InternetLogParser(in string inputText)
        {
            InputText = inputText;
        }
        public string InputText { get; }
        public Logger Logger { get; set; } = Logger.Dummylogger;


        string GetSubstringBetween(int startIndex, in string searchPredicateFront, in string searchPredicateBack)
        {
            int searchIndexFront = InputText.IndexOf(searchPredicateFront, startIndex, InputText.Length - startIndex);
            if (searchIndexFront == -1) throw new Exception($"{searchIndexFront} not found");

            int substringStart = searchIndexFront + searchPredicateFront.Length;

            int searchIndexBack = InputText.IndexOf(searchPredicateBack, substringStart, InputText.Length - substringStart);
            if (searchIndexBack == -1) throw new Exception($"{searchPredicateBack} not found");

            return InputText.Substring(substringStart, searchIndexBack - substringStart);
        }

        int FindStartOfNextDatapoint(int startIndex)
        {
            return InputText.IndexOf("//#!", startIndex, InputText.Length - startIndex);
        }

        int FindStartOfNextTest(int startIndex)
        {
            return InputText.IndexOf("//##", startIndex, InputText.Length - startIndex);
        }


        public IEnumerable<TestColumn> ParseTest(int startIndex)
        {
            var testName = GetSubstringBetween(startIndex, " ", ":");
            var coreCommand = GetSubstringBetween(startIndex, ": ", " ");
            Logger.Log($"    Looking at Test {testName} - coreCommand: {coreCommand}");
            switch (coreCommand)
            {
                case "./speedtest.py":
                    return ParseSpeedtest(startIndex, testName);
                case "ping":
                    return ParsePing(startIndex, testName);
                default:
                    Logger.Warning($"Core Command unkown");
                    return new List<TestColumn>();
            }
        }

        public IEnumerable<TestColumn> ParseSpeedtest(int startIndex, in string testName)
        {
            var pingString = GetSubstringBetween(startIndex, "Ping: ", " ms\n");
            var downloadString = GetSubstringBetween(startIndex, "Download: ", " Mbit/s\n");
            var uploadString = GetSubstringBetween(startIndex, "Upload: ", " Mbit/s\n");

            var result = new List<TestColumn>();
            result.Add(new TestColumn($"{testName}_ping[ms]", pingString));
            result.Add(new TestColumn($"{testName}_download[Mbit/s]", downloadString));
            result.Add(new TestColumn($"{testName}_upload[Mbit/s]", uploadString));
            return result;
        }

        public IEnumerable<TestColumn> ParsePing(int startIndex, in string testName)
        {
            var packetLossString = GetSubstringBetween(startIndex, "received, ", "% packet loss");
            //todo take care of unsucessful pings
            var pingString = GetSubstringBetween(startIndex, "min/avg/max/mdev = ", " ms");
            var averagePing = pingString.Split('/').ElementAt(1);

            var result = new List<TestColumn>();
            result.Add(new TestColumn($"{testName}_packetLoss[%]", packetLossString));
            result.Add(new TestColumn($"{testName}_averadgePing[ms]", averagePing));
            return result;
        }


        public List<Datapoint> Parse()
        {
            var result = new List<Datapoint>();

            int currentDatapointStart = FindStartOfNextDatapoint(0);
            do
            {
                int nextDatapointStart = FindStartOfNextDatapoint(currentDatapointStart + 1);

                var timeString = GetSubstringBetween(currentDatapointStart, "Time: ", "\n");
                Logger.Log($"Looking at Datapoint @{timeString}");

                var currentTestColumns = new List<TestColumn>();

                int currentTestStart = FindStartOfNextTest(currentDatapointStart);
                do
                {
                    int nextTestStart = FindStartOfNextTest(currentTestStart + 1);

                    currentTestColumns.AddRange(ParseTest(currentTestStart));

                    currentTestStart = nextTestStart;
                } while (currentTestStart < nextDatapointStart);

                result.Add(new Datapoint(timeString, currentTestColumns));
                currentDatapointStart = nextDatapointStart;
            } while (currentDatapointStart != -1);

            Logger.Log($"\nFound {result.Count} Datapoints");
            return result;
        }

    }
}
