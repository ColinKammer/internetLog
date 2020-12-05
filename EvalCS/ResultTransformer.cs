using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace EvalCS
{
    class ResultTransformer
    {
        public Logger Logger { get; set; }

        public List<string> Columns { get; }

        public List<InternetLogParser.Datapoint> ParsedLog { get; }

        public ResultTransformer(List<InternetLogParser.Datapoint> parsedLog, Logger logger = null)
        {
            if (logger is null) logger = Logger.Dummylogger;
            Logger = logger;

            ParsedLog = parsedLog;
            Columns = FindColumns(parsedLog);
        }

        private List<string> FindColumns(List<InternetLogParser.Datapoint> parsedLog)
        {
            var columns = new List<string>();

            Logger.Log($"Searching Columns...");
            foreach (var dp in parsedLog)
            {
                foreach (var column in dp.TestColumns)
                {
                    if (columns.Contains(column.Name) == false)
                    {
                        columns.Add(column.Name);
                    }

                }
            }
            return columns;
        }

        public string ToCsv(char cellSperator, char lineSperator)
        {
            var builder = new StringBuilder();

            //Add Title Row
            builder.Append("Time").Append(cellSperator);
            foreach (var columnName in Columns)
                builder.Append(columnName).Append(cellSperator);
            builder.Append(lineSperator);

            //Add Data
            foreach (var dp in ParsedLog)
            {
                //Add Line
                builder.Append(dp.Time).Append(cellSperator);
                foreach (var columnName in Columns)
                {
                    var matchingColumn = dp.TestColumns.FirstOrDefault(x => x.Name == columnName);
                    if (matchingColumn != null) builder.Append(matchingColumn.Value);
                    builder.Append(cellSperator);
                }
                builder.Append(lineSperator);
            }

            return builder.ToString();
        }
    }
}
