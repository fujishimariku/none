import boto3
import contextlib
import datetime as dt

#音声合成
#テキスト内容とボイスIDを取得し結果を返す
def polly(text, languagecode):
    polly = boto3.client('polly')

    #結果を取得
    result = polly.synthesize_speech(
        Text=text, OutputFormat='mp3', VoiceId=languagecode)

    #テキスト名から時間に変えました。
    now = dt.datetime.now()
    time = now.strftime('%Y%m%d-%H%M%S')

    #ファイルパス
    path = f"static/audio/{time}.mp3"

    #保存
    with contextlib.closing(result['AudioStream']) as stream:
        with open(path, 'wb') as file:
            file.write(stream.read())

    #ファイルパスを戻す
    return path
