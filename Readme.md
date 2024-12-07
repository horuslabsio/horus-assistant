# Horus Assistant

Hey there, I know you're lazy to check the company's wiki, so just ask me instead?

🤨 How can I apply for a vacation leave?
🏖️ Will the company sponsor my upcoming holiday to the Bahamas?
👩‍💻 Who can I contact to help debug my JS issues?

I've got an answer to all your questions..just ping me on Slack!

## Installation
**Prerequisites**
- Sign up on OpenAI, get some credits, find your key
- Sign up on Pinecone
- Create a Firecrawl account
- Create your slack app, get your keys

**Fill in your env variables**
```shell
OPENAI_API_KEY=
PINECONE_API_KEY=
FIRECRAWL_API_KEY=
SLACK_BOT_TOKEN=
SLACK_SIGNING_SECRET=
```

## Run your app
Start `ngrok` to access your app on an external network:
```shell
ngrok http 8000
```

