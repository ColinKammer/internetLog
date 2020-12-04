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


        struct Intervall
        {
            public Intervall(int start, int end)
            {
                Start = start;
                End = end;
            }
            public int Start { get; set; }
            public int End { get; set; }


            public int Length
            {
                get { return End - Start + 1; }
            }
        }

        public InternetLogParser(in string inputText)
        {
            InputText = inputText;
        }
        public string InputText { get; }
        public Logger Logger { get; set; } = Logger.Dummylogger;


        string GetPositionStringFromIndex(int index)
        {
            var newlinesInfront = 0;
            for (int i = 0; i < index; i++)
            {
                if (InputText[i] == '\n') newlinesInfront++;
            }

            var textColumn = index - InputText.LastIndexOf('\n', index);
            return $"row {newlinesInfront} column {textColumn}";

        }

        string GetSubstringBetween(int startIndex, in string searchPredicateFront, in string searchPredicateBack)
        {
            return GetSubstringBetween(new Intervall(startIndex, InputText.Length - 1), searchPredicateFront, searchPredicateBack);
        }
        string GetSubstringBetween(in Intervall searchIntervall, in string searchPredicateFront, in string searchPredicateBack)
        {
            int searchIndexFront = InputText.IndexOf(searchPredicateFront, searchIntervall.Start, searchIntervall.Length);
            if (searchIndexFront == -1)
            {
                return null;
            }

            int substringStart = searchIndexFront + searchPredicateFront.Length;

            int searchIndexBack = InputText.IndexOf(searchPredicateBack, substringStart, searchIntervall.End - substringStart);
            if (searchIndexBack == -1)
            {
                return null;
            }

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


        IEnumerable<TestColumn> ParseTest(in Intervall testIndecies)
        {
            var testName = GetSubstringBetween(testIndecies, " ", ":");
            var coreCommand = GetSubstringBetween(testIndecies, ": ", " ");
            Logger.Log($"    Looking at Test {testName} - coreCommand: {coreCommand}");
            switch (coreCommand)
            {
                case "./speedtest.py":
                    return ParseSpeedtest(testIndecies, testName);
                case "ping":
                    return ParsePing(testIndecies, testName);
                default:
                    Logger.Warning($"Core Command unkown");
                    return new List<TestColumn>();
            }
        }

        IEnumerable<TestColumn> ParseSpeedtest(in Intervall testIndecies, in string testName)
        {
            var result = new List<TestColumn>();

            var pingString = GetSubstringBetween(testIndecies, "Ping: ", " ms\n");
            var downloadString = GetSubstringBetween(testIndecies, "Download: ", " Mbit/s\n");
            var uploadString = GetSubstringBetween(testIndecies, "Upload: ", " Mbit/s\n");

            if (pingString is null && downloadString is null && uploadString is null)
            {
                Logger.Warning($"Speedtest failed in {GetPositionStringFromIndex(testIndecies.Start)}");
                return result;
            }

            if (pingString?.Length <= "1234.678".Length)
                result.Add(new TestColumn($"{testName}_ping[ms]", pingString));
            else
                Logger.Warning($"Unplausable value for Ping: {pingString}");

            if (downloadString?.Length <= "1234.678".Length)
                result.Add(new TestColumn($"{testName}_download[Mbit/s]", downloadString));
            else
                Logger.Warning($"Unplausable value for DownloadSpeed: {downloadString}");


            if (uploadString?.Length <= "1234.678".Length)
                result.Add(new TestColumn($"{testName}_upload[Mbit/s]", uploadString));
            else
                Logger.Warning($"Unplausable value for UploadSpeed: {uploadString}");


            return result;
        }

        IEnumerable<TestColumn> ParsePing(in Intervall testIndecies, in string testName)
        {
            var result = new List<TestColumn>();

            var packetLossString = GetSubstringBetween(testIndecies, "received, ", "% packet loss");
            if (packetLossString is null)
            {
                Logger.Warning($"Unable to find \"received, \" or \" % packet loss\" " +
                        $"between {GetPositionStringFromIndex(testIndecies.Start)} " +
                        $"and {GetPositionStringFromIndex(testIndecies.End)}"
                );
                return result;

            }

            if (packetLossString.Length <= "100".Length)
            {
                result.Add(new TestColumn($"{testName}_packetLoss[%]", packetLossString));
                if (packetLossString == "100")
                {
                    return result;
                }
            }
            else if (packetLossString.Contains("errors"))
            {
                packetLossString = GetSubstringBetween(testIndecies, "errors ", "% packet loss");
                result.Add(new TestColumn($"{testName}_packetLoss[%]", packetLossString));
                return result;
            }
            else
            {
                Logger.Error($"Unplausable value for Packetloss: {packetLossString}");
            }

            var pingString = GetSubstringBetween(testIndecies, "min/avg/max/mdev = ", " ms");
            if (pingString is null)
            {
                Logger.Error($"Unable to find \"min/avg/max/mdev = \" or \" ms\" " +
                    $"between {GetPositionStringFromIndex(testIndecies.Start)} " +
                    $"and {GetPositionStringFromIndex(testIndecies.End)}"
                );
                return result;
            }
            if (pingString.Length <= "012.2345/734.8993/243.3453/732.8901".Length)
            {
                var averagePing = pingString.Split('/').ElementAt(1);
                result.Add(new TestColumn($"{testName}_averadgePing[ms]", averagePing));
            }
            else
            {
                Logger.Warning($"Unplausable value for PingString: {pingString}");
            }
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

                    var currentTestIndecies = new Intervall(currentTestStart, nextTestStart - 1);
                    currentTestColumns.AddRange(ParseTest(currentTestIndecies));

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
