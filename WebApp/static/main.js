var accountModalBtn = document.querySelector(".account-modal-btn");
var accountModal = document.getElementById("accountModal");
var overlay = document.getElementById('overlay');
var body = document.body;
var navBar = document.querySelector(".app-bar")

accountModalBtn.addEventListener("click", function() {
    accountModal.style.display = 'block';
    overlay.style.display = 'block'; // 어두운 오버레이 표시
    body.style.backgroundColor = 'rgba(0, 0, 0, 0.65)'; // 기존 창 어둡게
    navBar.style.backgroundColor = 'rgba(0, 0, 0, 0.65)';
});

// 모달 닫기
function closeModal() {
    accountModal.style.display = 'none';
    overlay.style.display = 'none'; // 어두운 오버레이 감추기
    body.style.backgroundColor = '#fff'; // 기존 창 밝게
    navBar.style.backgroundColor = '#F3E5FA';
}

// 모달 외의 영역 클릭 시 모달 닫기 (선택 사항)
$(document).mouseup(function (e){
    var LayerPopup = $("#accountModal");
    if(LayerPopup.has(e.target).length === 0){
      closeModal();
    }
});

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