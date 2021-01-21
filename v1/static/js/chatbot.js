const apiClient = axios.create({
    baseURL: "http://127.0.0.1:5000",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json"
    }
});

var outputArea = $("#chat-output");
var context_state = null;
var bot_name = "ChatBot";
var user_name = "";

function randomInteger(min, max) {
    var number = Math.floor(Math.random() * (max - min + 1)) + min;
    return number;
}

function processPlaceholders(response_message) {
    if(response_message.includes("<bot_name>")) {
        response_message = response_message.replace("<bot_name>", bot_name);
    }
    if(response_message.includes("<user_name>")) {
        response_message = response_message.replace("<user_name>", user_name);
    }
    if(response_message.includes("<time_of_day>")) {
        var today = new Date();
        var currentHour = today.getHours();
        var time_of_day = "day";
        
        if (currentHour < 12) {
          time_of_day = "morning";
        } else if (currentHour < 18) {
          time_of_day = "afternoon";
        } else {
          time_of_day = "evening";
        }
        response_message = response_message.replace("<time_of_day>", time_of_day);
    }
    if(response_message.includes("<current_time>")) {
        var time = new Date();
        var current_time = time.toLocaleString('en-US', {
            hour: 'numeric', minute: 'numeric', hour12: true });
        response_message = response_message.replace("<current_time>", current_time);
    }
    return response_message;
}

function checkContextForUser(message) {
    if(context_state && context_state == "what_name") {
        filtered_message = message.replace("you can", "")
        filtered_message = filtered_message.replace("call me", "")
        filtered_message = filtered_message.replace("my name is", "")
        filtered_message = filtered_message.trim()
        user_name = filtered_message
        message = "my name is"
    }
    return message;
}

$("#user-input-form").on("submit", function(e) {
  
  e.preventDefault();
  
  var message = $("#user-input").val();

  outputArea.append(`
    <div class='bot-message'>
      <div class='message'>
        ${message}
      </div>
    </div>
  `);

  message = checkContextForUser(message);

  payload = JSON.stringify({
    "message": message.toLowerCase(),
    "context_state": context_state
  });

  apiClient.post('/bot', payload)
    .then(response => {
        // console.log(response.data);
        var response_message = response.data['message'];
        context_state = response.data['context_state'];
        response_message = processPlaceholders(response_message);

        setTimeout(function() {
            outputArea.append(`
              <div class='user-message'>
                <div class='message'>
                  ${response_message}
                </div>
              </div>
            `);
          }, randomInteger(2, 5) * 1000); // Random response time 2 - 5 seconds
            
    })
    .catch(error => {
        console.log('There was an error:', error.response);
    });
  
  $("#user-input").val("");
  
});