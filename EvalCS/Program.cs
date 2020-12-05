using System;
using System.Collections.Generic;
using System.Diagnostics;
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
            Logger logger = new Logger(
                log: x => Debug.WriteLine(x),
                warning: x => Console.WriteLine("WARNING: " + x),
                error: x => Console.WriteLine("SOFTERROR: " + x)
                );

            var logString = File.ReadAllText("results.txt"); //Todo: use console parameter

            var parser = new InternetLogParser(logString);
            parser.Logger = logger;
            var parsedLog = parser.Parse();

            var concentratedResult = new ResultTransformer(parsedLog);

            var csv = concentratedResult.ToCsv(';', '\n');
            File.WriteAllText("out.csv", csv); //Todo: use console parameter

            Console.WriteLine("DONE - PRESS ANY KEY");
            Console.ReadKey();
        }
    }
}
