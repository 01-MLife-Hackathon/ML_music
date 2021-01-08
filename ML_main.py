import asyncio, discord, youtube_dl
from discord.ext import commands

app = commands.Bot(command_prefix='ML ')

token = "Nzk3MTI2NzQ2NzYyOTAzNjAy.X_h8Ig.xqikUJz5RBZNtCjL-_T8xr8-mGc"
calcResult = 0


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
    if message.content == "ML 안녕":
        await message.channel.send("안녕 M-Life 친구들")
    if "ML 따라하기" in message.content:
        repeat = str(message.content).replace("ML 따라하기", "")
        await message.channel.send(repeat)


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
    # 오류 있음. 수정할 것.
    try:
        player = await app.voice_clients[0].create_ytdl_player(url)
        player.start()
    except Exception as Err:
        await ctx.send("```오류 메세지 : " + str(Err) + "```")


app.run(token)
