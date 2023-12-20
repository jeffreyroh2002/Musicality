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


function createPreferenceScales(prefDict, containerId) {
    const container = document.getElementById(containerId);

    for (let label in prefDict) {
        let score = prefDict[label];
        let prefContainer = document.createElement('div');
        prefContainer.classList.add('preference-container');

        let labelDiv = document.createElement('div');
        labelDiv.classList.add('preference-label');
        labelDiv.textContent = label;

        let scale = document.createElement('div');
        scale.classList.add('preference-scale');

        let positiveDiv = document.createElement('div');
        positiveDiv.classList.add('positive');
        positiveDiv.style.width = Math.max(0, score) + '%';

        let negativeDiv = document.createElement('div');
        negativeDiv.classList.add('negative');
        negativeDiv.style.width = Math.max(0, -score) + '%';

        scale.appendChild(negativeDiv);
        scale.appendChild(positiveDiv);
        prefContainer.appendChild(labelDiv);
        prefContainer.appendChild(scale);

        container.appendChild(prefContainer);
    }
}