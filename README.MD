sudo npm install -g redoc-cli

redoc-cli serve sms-platform.yaml

./prism-cli-linux mock sms-platform.yaml

 curl -X POST http://localhost:4010/send_sms \
          -u "test:test" \
          -H "Content-Type: application/json" \
          -d '{"sender": "test", "recipient": "89101335645", "message": "Hello"}'
{"status":"success","message_id":"123456"}