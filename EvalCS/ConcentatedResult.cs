using AntlrInternetLogParser;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace EvalCS
{
    class ConcentatedResult
    {
        class Column
        {
            string Name;
            Dictionary<string, double> Values = new Dictionary<string, double>();
        }

        List<Column> Columns = new List<Column>();

        public ConcentatedResult(InternetLogParser.FileContext parsedLog)
        {
            foreach (var dp in parsedLog.children)
            {

            }
        }
    }
}
