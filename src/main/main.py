import src.main.bot.adrenaline_bot as b
import src.main.user.admin as admin

LOPATA_ID = '448223022'
DK_ID = '427635051'
POLAND_ID = ''

bot = b.Adrenaline_bot()
bot.add_new_admin(admin.Admin(LOPATA_ID, 607, 'main'))
bot.add_new_admin(admin.Admin(DK_ID, 606, 'main'))
bot.start_bot()
