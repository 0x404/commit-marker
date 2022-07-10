CORRECTIVE: str = "Corrective"
PERFECTIVE: str = "Perfective"
ADAPTIVE: str = "Adaptive"
HEADERS: list = [
    "\ufeffID",
    "Hash",
    "Subject",
    "Message",
    "Num_files",
    "LOC",
    "changed files | + | -| sum",
    "Labels",
    "",
]
keywords = {
    CORRECTIVE: [
        "fix",
        "solve",
        "close",
        "handle",
        "issue",
        "defect",
        "bug",
        "problem",
        "ticket",
    ],
    PERFECTIVE: [
        "refactor",
        "re-factor",
        "reimplement",
        "re-implement",
        "design",
        "repace",
        "modify",
        "update",
        "upgrad",
        "cleanup",
        "clean-up",
    ],
    ADAPTIVE: [
        "add",
        "new",
        "introduce",
        "implement",
        "implemented",
        "extend",
        "feature",
        "support",
    ],
}
