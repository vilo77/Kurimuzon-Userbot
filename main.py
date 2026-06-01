import asyncio
import contextlib
import logging
import os
import pathlib
import platform
from pyrogram import Client, enums, idle
import git

os.chdir(pathlib.Path(__file__).parent)


async def main():
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[stdout_handler],
    )

    # Ambil SESSION_STRING dari environment variable
    SESSION_STRING = os.environ.get("SESSION_STRING") or os.environ.get("STRING_SESSION")

    if not SESSION_STRING:
        raise ValueError(
            "❌ SESSION_STRING tidak ditemukan!"
            "Set environment variable SESSION_STRING di Railway."
            "Generate session dulu pakai @OfficialPyrogramBot di Telegram."
        )

    logging.info("✅ SESSION_STRING ditemukan, memulai userbot...")

    # Hapus session file lama kalau ada
    session_file = pathlib.Path(__file__).parent / "KurimuzonUserbot.session"
    if session_file.exists():
        session_file.unlink()
        logging.info("✅ Deleted old session file")

    # Pakai Client langsung dari Pyrogram (bukan CustomClient)
    app = Client(
        "KurimuzonUserbot",
        session_string=SESSION_STRING,
        api_id=int(os.environ.get("API_ID", 6)),
        api_hash=os.environ.get("API_HASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e"),
        device_model="Samsung SM-F966B",
        system_version="16 (36)",
        app_version="12.3.1 (63852)",
        lang_pack="android",
        lang_code="id",
        plugins=dict(root="plugins"),
    )

    await app.start()

    logging.info("✅ Userbot berhasil start!")

    # Get dialogs (untuk confirm session aktif)
    async for _ in app.get_dialogs(limit=1):
        pass

    try:
        git.Repo()
    except git.exc.InvalidGitRepositoryError:
        repo = git.Repo.init()
        origin = repo.create_remote(
            "origin", "https://github.com/KurimuzonAkuma/Kurimuzon-Userbot"
        )
        origin.fetch()
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)

    await idle()

    await app.stop()


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        if platform.system() == "Windows":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        else:
            try:
                import uvloop
                uvloop.install()
            except ImportError:
                logging.warning("uvloop not installed.")

        if platform.python_version_tuple() >= ("3", "11"):
            with asyncio.Runner() as runner:
                loop = runner.get_loop()
                loop.run_until_complete(main())
        else:
            loop = asyncio.new_event_loop()
            loop.run_until_complete(main())
