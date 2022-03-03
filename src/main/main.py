import src.main.bot.adrenaline_bot as b
import src.main.user.admin as admin

LOPATA_ID = '448223022'
DK_ID = '427635051'
POLAND_ID = ''
PAY_URL = 'https://www.tinkoff.ru/rm/kravchenko.danila5/Nbfxk55061/'

bot = b.Adrenaline_bot()
bot.add_new_admin(admin.Admin(LOPATA_ID, PAY_URL, 607, 'main'))
bot.add_new_admin(admin.Admin(DK_ID, PAY_URL, 606, 'main'))
bot.start_bot()
