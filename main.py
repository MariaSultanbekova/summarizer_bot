import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
import telebot
import subprocess
import requests
from glob import glob
import os

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")



model_name = "t5-small"

# load tokenizer
tokenizer = T5Tokenizer.from_pretrained(model_name)

# load model
model = T5ForConditionalGeneration.from_pretrained(model_name)
model.to(device)

# load audio model
au_model, decoder, utils = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                          model='silero_stt',
                                          language='en',  # also available 'de', 'es'
                                          device='cpu')

(read_batch, split_into_batches,
 read_audio, prepare_model_input) = utils


with open('token_telebot.txt', 'r') as file:
    token = file.read()
bot = telebot.TeleBot(token)


def audio_to_text(path_to_audio, dest_filename='outputs.wav'):

    device = torch.device('cpu')  # gpu also works, but our models are fast enough for CPU
    decode_message = ''

    process = subprocess.run(['ffmpeg', '-i', path_to_audio, dest_filename])
    if process.returncode != 0:
        raise Exception("Something went wrong")


    test_files = glob(dest_filename)
    batches = split_into_batches(test_files, batch_size=10)
    input = prepare_model_input(read_batch(batches[0]),
                                device=device)

    output = au_model(input)

    for sample in output:
        decode_message += decoder(sample.cpu())

    os.remove(path_to_audio)
    os.remove(dest_filename)

    return decode_message


def generate(text, **kwargs):
    inputs = tokenizer(text, return_tensors='pt')
    with torch.no_grad():
        hypotheses = model.generate(**inputs,
                                    num_beams=4,
                                    **kwargs,
                                    no_repeat_ngram_size=2,
                                    min_length=30,
                                    max_length=100,
                                    early_stopping=True)
    return tokenizer.decode(hypotheses[0], skip_special_tokens=True)



@bot.message_handler(content_types=['text'])
def get_user_message(message):
    bot.send_message(message.chat.id,
                    f"Oh hey! I am a bot that will help you save your time")


@bot.message_handler(content_types=['voice'])
def get_user_audio(message):
    bot.reply_to(message, 'The audio is being processed...')
    try:
        file_info = bot.get_file(message.voice.file_id)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))

        with open('voice.ogg', 'wb') as f:
            f.write(file.content)

        text = audio_to_text('voice.ogg')
        text = 'summarize: ' + text

        summary = generate(text)
        bot.send_message(message.from_user.id, summary)


    except Exception as e:
        bot.reply_to(message, e)


bot.polling(none_stop=True)
