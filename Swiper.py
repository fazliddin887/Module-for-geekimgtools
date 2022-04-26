#meta developer: 𝙰𝚖𝚘𝚛𝚎 𝚏𝚘𝚛𝚎𝚟𝚎𝚛🌘


from .. import loader, utils
import logging
from PIL import Image, ImageOps
import io

logger = logging.getLogger(__name__)

@loader.tds
class GiftoolMod(loader.Module):
	"""Giftool
	developer: @the_farkhodov"""
	strings = {
		"name": "Swiper"
	}

	async def client_ready(self, client, db):
		self.client = client
	
	
	@loader.owner
	async def sl2rcmd(self, message):
		"""поворот на ➡️"""
		await presser(message, 0)
		
	@loader.owner
	async def sr2lcmd(self, message):
		"""поворос ⬅️"""
		await presser(message, 1)
		
	@loader.owner
	async def su2dcmd(self, message):
		"""поворот в ⬇️"""
		await presser(message, 2)
		
	@loader.owner
	async def sd2ucmd(self, message):
		"""swipe down to up"""
		await presser(message, 3)
		
async def check_media(message):
	reply = await message.get_reply_message()
	if not reply:
		return False
	if not reply.file:
		return False
	mime = reply.file.mime_type.split("/")[0].lower()
	if mime != "image":
		return False
	return reply
	
	
async def presser(message, way):
	reply = await check_media(message)
	if not reply:
		await message.edit("<b>Сенпай... пожалуйста, ответьте на картинку или не анимированную наклейку !</b>")
		return
	im = io.BytesIO()
	await reply.download_media(im)
	im = Image.open(im)
	w, h = im.size
	out = []
	await message.edit("<b>Ждите работа тяжёлая💾...</b>")
	if way == 0:
		for x in range(1, w, w//30):
			im1 = im2 = im.copy()
			temp = Image.new("RGB", (w, h))
			im1 = im1.resize((x, h))
			im2 = im2.resize((w-x, h))
			temp.paste(im1, (0, 0))
			temp.paste(im2, (x, 0))
			out.append(temp)
			
	if way == 1:
		for x in range(1, w, w//30):
			im1 = im2 = im.copy()
			temp = Image.new("RGB", (w, h))
			im1 = ImageOps.mirror(im1.resize((x, h)))
			im2 = ImageOps.mirror(im2.resize((w-x, h)))
			temp.paste(im1, (0, 0))
			temp.paste(im2, (x, 0))
			temp = ImageOps.mirror(temp)
			out.append(temp)
			
	if way == 2:
		for y in range(1, h, h//30):
			im1 = im2 = im.copy()
			temp = Image.new("RGB", (w, h))
			im1 = im1.resize((w, y))
			im2 = im2.resize((w, h-y))
			temp.paste(im1, (0, 0))
			temp.paste(im2, (0, y))
			out.append(temp)
			
	if way == 3:
		for y in range(1, h, h//30):
			im1 = im2 = im.copy()
			temp = Image.new("RGB", (w, h))
			im1 = ImageOps.flip(im1.resize((w, y)))
			im2 = ImageOps.flip(im2.resize((w, h-y)))
			temp.paste(im1, (0, 0))
			temp.paste(im2, (0, y))
			temp = ImageOps.flip(temp)
			out.append(temp)
			
	output = io.BytesIO()
	output.name = "output.gif"
	out[0].save(output, save_all=True, append_images=out[1:], duration=1)
	output.seek(0)
	await reply.reply(file=output)
	await message.delete()
	