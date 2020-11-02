from scripts.lib.SendEmail import SendEmail
import json

with open('security/credentials.txt', 'rb') as json_file:
    cred = json.load(json_file)
    user = cred['User']
    pwd = cred['Password']

se = SendEmail(user=user, pwd=pwd, client='smtp.office365.com')


ls_imgs = ['src/img/squares.gif',
           'src/img/logo-kg.png',
           'src/img/scores_ts.png',
           'src/img/contrib_pie.png']

ls_ids = ['header', 'logo', 'scores_ts', 'pie']

d_images = dict(zip(ls_ids, ls_imgs))

ls_data = ['src/other/team_230618.xlsx']

html_txt = '''
        <html lang="es">
            <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <title>Predictland – Hour Report</title>
            </head>

            <table style='background-color: #000000; width: 100%'>
            <td align='center' bgcolor='#000000' style='height: 25%;'>
                <p>
                <img src='cid:{}' alt='Creating Email Magic' width='1239' height='567.88'/>
                </p>
                <p>
                <a href="https://www.kaggle.com/" class="navbar-brand custom-logo-link default-logo" rel="home">
                                        
                <svg width="180px" height="36px" viewBox="0 0 180 36" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                    <g id="Symbols" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                        <g id="Logotipo-horizontal" fill="#FFFFFF">
                            <img src='cid:{}'>
                            </g>
                        </g>
                    </g>
                </svg>					</a>
                
                </p>        
                        <p style='color:#ffffff; font-weight: bold; font-size:50px'>Dear Team,</p>
                        <p style='color:#ffffff; font-weight: bold; font-size:50px'>Here you have the daily status Newsletter</p>

                <br><img src="cid:{}"><br>
                <br><img src="cid:{}"><br>

                <p style='color:#ffffff; font-weight: bold; font-size:30px'>Kind Regards</p>
                </td>
                <p>&nbsp</p>
                </td>
            </table>
            </html>
            '''.\
                format(*d_images.keys())


email_msg = se.generate_email(html_txt=html_txt,
                              subject='Daily Newsletter',
                              to_list=[user],
                              data_paths=ls_data)

for id, path in d_images.items():
    se.attach_image(email_msg, path, id)

se.send_email(email_msg)