import asyncio, discord, youtube_dl
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

app = commands.Bot(command_prefix='ML ')
token = "Token Here"

playerlist = []
playlist = []
que = {}


def queue(id):  # 음악 재생용 큐
    if que[id] != []:
        player = que[id].pop(0)
        playerlist[id] = player
        del playlist[0]
        player.start()


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
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(app.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
    else:
        await ctx.send("리스트에 추가되었습니다.")
        return


app.run(token)
