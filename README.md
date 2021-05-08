# F312

Framework to implement file types with load/save/init option.

**Disclaimer** I find myself wanting to kill this package. I feel that my evolution as a programmer compels me to not 
want to publish APIs that implement layers over well established resources (in this case SQLite); furthermore the 
different components don't go well together, as sqlite files do not have this concept of save/load right? I find myself
now just implementing my new version(s) of a FileSQLite (or whatever) for my most serious packages. Again it is OK to 
wrap established resources/packages/classes; I just do not think that it justifies a standalone project.
