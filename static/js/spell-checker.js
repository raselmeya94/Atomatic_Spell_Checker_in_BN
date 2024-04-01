$(document).ready(function() {
    // count misspelled word
    let countMisspelled = 0;
    let previousText = "";

    $('#textArea').on('input', function(event) {
        let text = $('#textArea').val().trim();
        if (text !== previousText && text.endsWith(' ')) {
            previousText = text;
            spellCheck();
        }
    });

    $('#textArea').on('keyup', function(event) {
        if (event.keyCode === 32) {
            spellCheck();
        }
    });

    function spellCheck() {
        let text = $('#textArea').val().trim();

        let lastSpaceIndex = text.lastIndexOf(' ');
        let currentWord = lastSpaceIndex !== -1 ? text.substring(lastSpaceIndex + 1) : text;

        if (currentWord.trim() === '') {
            return;
        }

        $.ajax({
            type: 'POST',
            url: '/correct_spelling',
            data: JSON.stringify({text: currentWord}),
            contentType: 'application/json',
            success: function(data) {
                let correctedWord = data.corrected_text;
                let correctedText = text.substring(0, lastSpaceIndex + 1) + correctedWord;

                if (correctedWord !== currentWord && correctedWord !== "") {
                    countMisspelled++;
                    
                    
                }
                $('#textArea').val(correctedText+" ");

                $('#misspelledCount').text("Misspelled words count: " + countMisspelled);
            }
        });
    }
});
