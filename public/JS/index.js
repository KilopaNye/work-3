document.getElementById('uploadButton').addEventListener('click', function () {
    let fileInput = document.getElementById('imageInput');
    let inputMessage = document.querySelector("#inputMessage")
    let file = fileInput.files[0];
    let message = inputMessage.value
    if (message != "") {
        if (file) {
            let formData = new FormData();
            formData.append('file', file);
            formData.append('message', message);
            fetch('/api/upload', {
                method: 'POST',
                headers: { 'enctype': "multipart/form-data" },
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    // window.location.href="/";
                    loadingPage()
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        } else {
            let formData = new FormData();
            formData.append('message', message);
            fetch('/api/upload', {
                method: 'POST',
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    // window.location.href="/";
                    loadingPage()
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    } else {
        alert("訊息不得為空")
    }
});

function loadingPage() {
    let root = document.querySelector(".root")
    root.innerHTML=""
    let headers = {
        "Content-Type": "application/json",
    };
    fetch('/api/loading', {
        method: "GET",
        headers: headers
    }).then(response => response.json()).then(data => {
        for (let i = 0; i < data['data'].length; i++) {
            let root = document.querySelector('.root')
            let messageDiv = document.createElement('div')
            root.appendChild(messageDiv)
            let messageTxt = document.createElement('div')
            messageTxt.textContent = data['data'][i]['message']
            messageTxt.classList.add("txt")
            messageDiv.appendChild(messageTxt)
            if (data['data'][i]['image_id'] != null) {
                let messageImage = document.createElement('img')
                messageImage.src = "https://d3utiuvdbysk3c.cloudfront.net/" + data['data'][i]['image_id']
                messageImage.classList.add("message-img")
                messageDiv.appendChild(messageImage)
            }
            let messageHr = document.createElement('hr')
            messageDiv.appendChild(messageHr)
        }
    }
    ).catch(error => {
        console.error(error)
    })
}
loadingPage()