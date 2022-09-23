# vosk-asr
This project uses `docker-compose.yaml` to deploy vosk server for transcription and vosk-recasepunc for recasing text and 
adding punctuation.

vosk-server has exposed a websocket server at port `2700`. This vosk websocket server can be integrated directly with freeswitch, jitsi jigasi, asterisk for speech recognition.

vosk-recasepunc is being served using HTTP at port `8081`.

# vosk-recasepunc API

It has exposed only one HTTP endpoint.

POST `/vosk/transcription/recase-punc`.

Both request body and response body use `application/json`.

Sample request body
```json
{
    "data": [
        {
            "text": "the person that extension one zero one he's unavailable"
        },
        {
            "text": "hello world i am here"
        }
    ]
}
```

Sample response body
```json
{
    "data": [
        {
            "text": "The person that extension one zero one he's unavailable."
        },
        {
            "text": "Hello world, I am here."
        }
    ]
}
```