import asyncio, discord, threading, time
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

app = commands.Bot(command_prefix='ML ')
token = ""

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

playlist = []


def play():
    player = playlist.pop(0)
    print("player :", player, '\n', len(playlist))
    player[0].play(FFmpegPCMAudio(player[1], **FFMPEG_OPTIONS))


def _play():
    while True:
        if len(playlist) == 0:
            print('threading off')
            return
        if not playlist[0][0].is_playing():  # 만약 플레이중이 아니면
            play()
        else:
            pass
        time.sleep(10)


def add(player, URL):  # 플레이할 곡 정보를 리스트에 저장
    thread = 0
    if len(playlist) == 0:
        thread = 1

    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(URL, download=False)
    URL = info['formats'][0]['url']
    playlist.append((player, URL))

    if thread and not playlist[0][0].is_playing():  # 첫 한번 멀티쓰레딩
        print("Therading on")
        thread = threading.Thread(target=_play)
        thread.start()
        return 0

    return 1


@app.event
async def on_ready():
    # 봇이 정상적으로 켜졌는지 확인
    print("다음으로 로그인합니다 : ")
    print(app.user.name)
    print(app.user.id)
    print("==========")
    game = discord.Game("'ML 도와줘' 를 입력하세요. Made By H0N9_D4N")
    await app.change_presence(status=discord.Status.online, activity=game)  # 바뀜


@app.event
async def on_message(message):
    await app.process_commands(message)
    if message.author.bot:
        return None
    if message.content == "시발":
        await message.channel.send("빠르고 꼬운 말")


@app.command(name="도와줘")
async def _help(ctx):
    ret = "```\n" \
          "M-Life Music bot By H0N9D4N\n" \
          "USAGE :\n" \
          "ML 안녕\n" \
          "ML 따라하기 <str>\n" \
          "ML 이리온\n" \
          "ML 저리가\n" \
          "ML 노래해 <링크>\n" \
          "ML 잠깐만\n" \
          "ML 다시\n" \
          "ML 목록\n" \
          "이스터에그 1추\n" \
          "```"
    await ctx.send(ret)
    

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
    playlist.clear()
    await app.voice_clients[0].disconnect()  # 채널에서 나가기


@app.command(name="노래해", pass_context=True)
async def _sing(ctx, url):
    voice = get(app.voice_clients, guild=ctx.guild)
    if add(voice, url):
        await ctx.send("리스트에 노래를 추가하였습니다.")


@app.command(name="잠깐만")
async def _pause(ctx):
    try:
        if playlist[0][0].is_paused():
            await ctx.send("이미 멈춰있네용")
        else:
            playlist[0][0].pause()
            await ctx.send("잠깐만!")
    except:
        await ctx.send("뭐야 아무것도 없잖아")


@app.command(name="다시")
async def _resume(ctx):
    try:
        if playlist[0][0].is_playing():
            await ctx.send("이미 재생중인걸")
        else:
            playlist[0][0].resume()
            await ctx.send("다시!")

    except:
        await ctx.send("뭐야 아무것도 없잖아")


@app.command(name="목록")
async def _list_song(ctx):
    cnt = str(len(playlist)) + " 개의 음악이 남았습니다."
    await ctx.send(cnt)


app.run(token)
