using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace EvalCS
{
    class Logger
    {
        public static readonly Logger Dummylogger = new Logger(x => { }, x => { }, x => { });

        public Logger(Action<string> log, Action<string> warning, Action<string> error)
        {
            Log = log;
            Warning = warning;
            Error = error;
        }

        public Action<string> Log { get; }
        public Action<string> Warning { get; }
        public Action<string> Error { get; }
    }
}
