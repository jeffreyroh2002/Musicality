var once = true;

function OnlyOneClick() {
    if (once) {
        once = false; // if clicked once, then block the button
        return true;
    } 
    else {
        return false; // False means block
    }}

        
var id = document.getElementById('button1');

id.addEventListener('click', function () {
    var ooc = OnlyOneClick();
    if (ooc === false) {
        document.getElementById('button1').disabled = true;
    }
})
