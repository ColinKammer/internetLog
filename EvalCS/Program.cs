using Antlr4.Runtime;
using AntlrInternetLogParser;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace EvalCS
{
    class Program
    {


        static void Main(string[] args)
        {
            var logString = File.ReadAllText("results.txt"); //Todo: use console parameter

            var inputStream = new AntlrInputStream(logString);
            var lexer = new InternetLogLexer(inputStream);
            var tokenStream = new CommonTokenStream(lexer);
            var parser = new InternetLogParser(tokenStream);
            var parsedLog = parser.file();

            var concentratedResult = new ConcentatedResult(parsedLog);

        }
    }
}
