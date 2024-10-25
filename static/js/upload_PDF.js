document.getElementById('uploadForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const fileInput = document.getElementById('fileInput');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('/translate_PDF/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Ошибка при загрузке файла');
        }

        const data = await response.json();
        const downloadLink = document.getElementById('downloadLink');
        const downloadButton = document.getElementById('downloadButton');

        downloadButton.href = `/translate_PDF/download/${data.filename}`;
        downloadLink.classList.remove('hidden');
    } catch (error) {
        alert(error.message);
    }
});