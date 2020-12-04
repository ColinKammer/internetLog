echo Running Antlr Code Generation
antlrv4 -o AntlrInternetLogParser -Dlanguage=CSharp -package AntlrInternetLogParser -no-listener -visitor InternetLog.g4