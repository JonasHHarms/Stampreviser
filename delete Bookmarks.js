/* löscht alle automatischen Lesezeichen */
for (a = 0; a < 10; a++) { 
var bm = this.bookmarkRoot;
function deletelower(Bm)
{
if (Bm.children != null)
{ 
Bm.children[0].remove();
}
}
var root = this.bookmarkRoot;
if (root.children != null)
{ 
for (var i = 0; i < root.children.length; i++)
{ 
deletelower(root.children[i]);
}
}
}
