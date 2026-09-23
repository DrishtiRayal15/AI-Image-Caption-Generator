const fileInput =
    document.getElementById("fileInput");

const dropzone =
    document.getElementById("dropzone");

const dropzoneText =
    document.getElementById("dropzoneText");

const previewArea =
    document.getElementById("previewArea");

const previewImage =
    document.getElementById("previewImage");

const generateBtn =
    document.getElementById("generateBtn");

const loading =
    document.getElementById("loading");

const resultBox =
    document.getElementById("resultBox");

const captionText =
    document.getElementById("captionText");

const errorBox =
    document.getElementById("errorBox");


let selectedFile = null;


function resetPanels() {

    resultBox.hidden = true;

    errorBox.hidden = true;

}


function handleFile(file) {

    if (!file) {
        return;
    }


    if (!file.type.startsWith("image/")) {

        errorBox.textContent =
            "Please select a valid image file.";

        errorBox.hidden = false;

        return;
    }


    selectedFile = file;


    const reader =
        new FileReader();


    reader.onload = function(event) {

        previewImage.src =
            event.target.result;

        previewArea.hidden = false;

        dropzoneText.textContent =
            file.name;

    };


    reader.readAsDataURL(file);


    generateBtn.disabled = false;

    resetPanels();
}


fileInput.addEventListener(
    "change",
    function(event) {

        handleFile(
            event.target.files[0]
        );

    }
);


["dragenter", "dragover"].forEach(
    function(eventName) {

        dropzone.addEventListener(
            eventName,
            function(event) {

                event.preventDefault();

                dropzone.classList.add(
                    "dragover"
                );

            }
        );

    }
);


["dragleave", "drop"].forEach(
    function(eventName) {

        dropzone.addEventListener(
            eventName,
            function(event) {

                event.preventDefault();

                dropzone.classList.remove(
                    "dragover"
                );

            }
        );

    }
);


dropzone.addEventListener(
    "drop",
    function(event) {

        const file =
            event.dataTransfer.files[0];

        handleFile(file);

    }
);


generateBtn.addEventListener(
    "click",
    async function() {

        if (!selectedFile) {
            return;
        }


        resetPanels();

        loading.hidden = false;

        generateBtn.disabled = true;


        const formData =
            new FormData();


        formData.append(
            "image",
            selectedFile
        );


        try {

            const response =
                await fetch(
                    "/caption",
                    {
                        method: "POST",
                        body: formData
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.error ||
                    "Something went wrong."
                );

            }


            captionText.textContent =
                data.caption;

            resultBox.hidden = false;

        }

        catch (error) {

            errorBox.textContent =
                error.message;

            errorBox.hidden = false;

        }

        finally {

            loading.hidden = true;

            generateBtn.disabled = false;

        }

    }
);
