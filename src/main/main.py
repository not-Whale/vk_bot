import src.main.bot.adrenaline_bot as b
import src.main.user.admin as admin

bot = b.Adrenaline_bot()
bot.add_new_admin(admin.Admin(448223022, '', 607, 'main'))
bot.start_bot()
