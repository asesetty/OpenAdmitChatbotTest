$(document).ready(function() {
    $('#chat-form').on('submit', function(e) {
        e.preventDefault();

        var userMessage = $('#message').val();
        $('#message').val('');

        // Append user's message to chat window
        $('#chat-messages').append('<div class="user-message"><p>' + userMessage + '</p></div>');
        scrollToBottom();

        // Send message to server
        $.ajax({
            url: '/get_response',
            method: 'POST',
            data: { message: userMessage },
            success: function(response) {
                // Append AI's response to chat window
                $('#chat-messages').append('<div class="ai-message"><p>' + response.message + '</p></div>');
                scrollToBottom();
            },
            error: function() {
                $('#chat-messages').append('<div class="ai-message"><p>There was an error processing your request.</p></div>');
                scrollToBottom();
            }
        });
    });

    function scrollToBottom() {
        $('.chat-window').scrollTop($('.chat-window')[0].scrollHeight);
    }
});
