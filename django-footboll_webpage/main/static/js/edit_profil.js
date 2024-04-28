const deleteParagraph = document.getElementById('delete-p');
const deleteDiv = document.getElementById('delete-div');
const deleteFinalBtn = document.getElementById('delete-final');
const cancelDelete = document.getElementById('cancel-delete');
const form = document.getElementById('form');
const coachHolder = document.getElementById('coach-holder');
const coachsDiv = document.getElementById('coachs-div');

form.addEventListener('submit', submitHandler);

function submitHandler(event) {
    event.preventDefault();
    $.ajax({
        type:'POST',
        url: "{% url 'coach' %}",
        data: $("#form").serialize(),
        dataType: 'json',
        success: function(response) {
            if (response.status === 1) {
                coachHolder.innerHTML += response.html;
                buttonsSet();
            }
            else {
                alert(response.msg)
            }
        }
    })}
cancelDelete.addEventListener('click', function() { toggleHidden(deleteDiv); });
deleteFinalBtn.addEventListener('click', function() {
    $.ajax({
        type: 'GET',
        url: this.getAttribute('link'),
        dataType: 'json',
        success: function (response) {
            if (response.status === 1) {
                const deleting = document.getElementById(response.id);
                deleting.remove()
                toggleHidden(deleteDiv);
            }
            else {
                alert(response.msg)
            }
        }
        })
})
buttonsSet()

function toggleHidden(element) {
    element.classList.toggle('hidden')
}
function addText(text, id) {
    deleteParagraph.textContent = text;
    deleteFinalBtn.setAttribute('link', `/delete_coach/${id}/`)
}


function buttonsSet() {
    const deleteDivs = document.querySelectorAll('.delete-coach');
    deleteDivs.forEach((div) => {
        const coachId = div.getAttribute('id');
        const coachName = div.getAttribute('coach-name');
        const coachCertified = div.getAttribute('coach-certified');
        const deleteBtn = document.querySelector(`#delete-${coachId}`);
        const updateBtn = document.querySelector(`#update-${coachId}`);
        const updateForm = document.querySelector(`#update-form-${coachId}`);
        const boolEl = document.querySelector(`#bool-${coachId}`);
        const closeUpdate = document.querySelector(`#close-update-${coachId}`);
        const updateFinal = document.querySelector(`#final-update-${coachId}`);

        updateFinal.addEventListener('click', function() {
            $.ajax({
                type: 'POST',
                url: this.getAttribute('link'),
            dataType: 'json',
            success: function (response) {
                if (response.status === 1) {
                    div.setAttribute('coach-certified', response.certified);
                    toggleHidden(updateForm);
                    toggleHidden(div);
                }
            }
        })})
        });
        
        closeUpdate.addEventListener('click', function() {
            toggleHidden(updateForm);
            toggleHidden(div);
        });

        updateBtn.addEventListener('click', function() {
            if (coachCertified === "False") {
                boolEl.checked = false
            }
            else {
                boolEl.checked = true
            }
            toggleHidden(updateForm);
            toggleHidden(div);
        });

        deleteBtn.addEventListener('click', function() {
            addText(coachName, coachId);
            toggleHidden(deleteDiv);
        });
    };