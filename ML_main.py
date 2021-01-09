import asyncio, discord, threading
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

app = commands.Bot(command_prefix='ML ')
token = "Nzk3MTI2NzQ2NzYyOTAzNjAy.X_h8Ig.py0NpcJgJnFKsC64n_7xtSok5W0"

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

playlist = []
PLAYING = 0


def play():
    while True:
        if len(playlist) == 0:
            return
        if not playlist[0][0].is_playing():  # 만약 플레이중이 아니면
            player = playlist.pop(0)
            print("player :", player, '\n', len(playlist))
            player[0].play(FFmpegPCMAudio(player[1], **FFMPEG_OPTIONS))
        else:
            pass


def add(player, URL):  # 플레이할 곡 정보를 리스트에 저장
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(URL, download=False)
    URL = info['formats'][0]['url']
    playlist.append((player, URL))
    for things in playlist:
        print("list :", things)

    if PLAYING == 0:  # 첫 한번 플레이중이 아니면 플레이 멀티스레딩 걸어놈
        thread = threading.Thread(target=play)
        thread.start()
        return 0
    if not playlist[0][0].is_playing():
        return 0

    return 1


@app.event
async def on_ready():
    # 봇이 정상적으로 켜졌는지 확인
    print("다음으로 로그인합니다 : ")
    print(app.user.name)
    print(app.user.id)
    print("==========")
    game = discord.Game("M-Life Music bot By H0N9D4N")
    await app.change_presence(status=discord.Status.online, activity=game)  # 바뀜


@app.event
async def on_message(message):
    await app.process_commands(message)
    if message.author.bot:
        return None


@app.command(name="안녕")
async def hi(ctx):
    await ctx.send("안녕 M-Life 친구들")


@app.command(name="따라하기")
async def repeat(ctx, *, txt):
    await ctx.send(txt)


@app.command(name="이리온", pass_context=True)
async def _join(ctx):
    if ctx.author.voice and ctx.author.voice.channel:  # 사용자가 들어간 채널 파악
        channel = ctx.author.voice.channel
        await channel.connect()  # 채널 연결
    else:  # 유저가 채널에 없으면
        await ctx.send("채널에 연결되지 않았습니다.")  # 출력


@app.command(name="저리가")
async def _leave(ctx):
    await app.voice_clients[0].disconnect()  # 채널에서 나가기


@app.command(name="노래해", pass_context=True)
async def _sing(ctx, url):
    voice = get(app.voice_clients, guild=ctx.guild)
    if add(voice, url):
        await ctx.send("리스트에 노래를 추가하였습니다.")


app.run(token)
