import os
from urllib.parse import quote

html = """
<html>
<head>

  <meta charset="utf-8">
  <meta http-equiv="x-ua-compatible" content="ie=edge">
  <title>Email Confirmation</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style type="text/css">
  /**
   * Google webfonts. Recommended to include the .woff version for cross-client compatibility.
   */
  @media screen {
    @font-face {
      font-family: 'Source Sans Pro';
      font-style: normal;
      font-weight: 400;
      src: local('Source Sans Pro Regular'), local('SourceSansPro-Regular'), url(https://fonts.gstatic.com/s/sourcesanspro/v10/ODelI1aHBYDBqgeIAH2zlBM0YzuT7MdOe03otPbuUS0.woff) format('woff');
    }
    @font-face {
      font-family: 'Source Sans Pro';
      font-style: normal;
      font-weight: 700;
      src: local('Source Sans Pro Bold'), local('SourceSansPro-Bold'), url(https://fonts.gstatic.com/s/sourcesanspro/v10/toadOcfmlt9b38dHJxOBGFkQc6VGVFSmCnC_l7QZG60.woff) format('woff');
    }
  }
  /**
   * Avoid browser level font resizing.
   * 1. Windows Mobile
   * 2. iOS / OSX
   */
  body,
  table,
  td,
  a {
    -ms-text-size-adjust: 100%; /* 1 */
    -webkit-text-size-adjust: 100%; /* 2 */
  }
  /**
   * Remove extra space added to tables and cells in Outlook.
   */
  table,
  td {
    mso-table-rspace: 0pt;
    mso-table-lspace: 0pt;
  }
  /**
   * Better fluid images in Internet Explorer.
   */
  img {
    -ms-interpolation-mode: bicubic;
  }
  /**
   * Remove blue links for iOS devices.
   */
  a[x-apple-data-detectors] {
    font-family: inherit !important;
    font-size: inherit !important;
    font-weight: inherit !important;
    line-height: inherit !important;
    color: inherit !important;
    text-decoration: none !important;
  }
  /**
   * Fix centering issues in Android 4.4.
   */
  div[style*="margin: 16px 0;"] {
    margin: 0 !important;
  }
  body {
    width: 100% !important;
    height: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
  }
  /**
   * Collapse table borders to avoid space between cells.
   */
  table {
    border-collapse: collapse !important;
  }
  a {
    color: #1a82e2;
  }
  img {
    height: auto;
    line-height: 100%;
    text-decoration: none;
    border: 0;
    outline: none;
  }
  </style>

</head>
<body style="background-color: #e9ecef;">

  <!-- start preheader -->
  <div class="preheader" style="display: none; max-width: 0; max-height: 0; overflow: hidden; font-size: 1px; line-height: 1px; color: #fff; opacity: 0;">
    A preheader is the short summary text that follows the subject line when an email is viewed in the inbox.
  </div>
  <!-- end preheader -->

  <!-- start body -->
  <table border="0" cellpadding="0" cellspacing="0" width="100%">
    <!-- start hero -->
    <tr>
      <td align="center" bgcolor="#e9ecef">
        <!--[if (gte mso 9)|(IE)]>
        <table align="center" border="0" cellpadding="0" cellspacing="0" width="600">
        <tr>
        <td align="center" valign="top" width="600">
        <![endif]-->
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
          <tr>
            <td align="left" bgcolor="#ffffff" style="padding: 36px 24px 0; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; border-top: 3px solid #d4dadf;">
              <h1 style="margin: 0; font-size: 32px; font-weight: 700; letter-spacing: -1px; line-height: 48px;">{title}</h1>
            </td>
          </tr>
        </table>
        <!--[if (gte mso 9)|(IE)]>
        </td>
        </tr>
        </table>
        <![endif]-->
      </td>
    </tr>
    <!-- end hero -->

    <!-- start copy block -->
    <tr>
      <td align="center" bgcolor="#e9ecef">
        <!--[if (gte mso 9)|(IE)]>
        <table align="center" border="0" cellpadding="0" cellspacing="0" width="600">
        <tr>
        <td align="center" valign="top" width="600">
        <![endif]-->
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">

          <!-- start copy -->
          <tr>
            <td align="left" bgcolor="#ffffff" style="padding: 24px; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; font-size: 16px; line-height: 24px;">
              <p style="margin: 0;">{main_message}</p>
            </td>
          </tr>
          <!-- end copy -->

          <!-- start button -->
          <tr>
            <td align="left" bgcolor="#ffffff">
              <table border="0" cellpadding="0" cellspacing="0" width="100%">
                <tr>
                  <td align="center" bgcolor="#ffffff" style="padding: 12px;">
                    <table border="0" cellpadding="0" cellspacing="0">
                      <tr>
                        <td align="center" bgcolor="#BA1546" style="border-radius: 6px;">
                          <a href="{action_url}" target="_blank" style="display: inline-block; padding: 16px 36px; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; font-size: 16px; color: #ffffff; text-decoration: none; border-radius: 6px;">{button_message}</a>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          <!-- end button -->

          <!-- start copy -->
          <tr>
            <td align="left" bgcolor="#ffffff" style="padding: 24px; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; font-size: 16px; line-height: 24px;">
              <p style="margin: 0;">{on_error_message}:</p>
              <p style="margin: 0;"><a href="{action_url}" target="_blank">{action_url}</a></p>
            </td>
          </tr>
          <!-- end copy -->

          <!-- start copy -->
          <tr>
            <td align="left" bgcolor="#ffffff" style="padding: 24px; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; font-size: 16px; line-height: 24px; border-bottom: 3px solid #d4dadf">
              <p style="margin: 0;">Cheers,<br> Paste</p>
            </td>
          </tr>
          <!-- end copy -->

        </table>
        <!--[if (gte mso 9)|(IE)]>
        </td>
        </tr>
        </table>
        <![endif]-->
      </td>
    </tr>
    <!-- end copy block -->

    <!-- start footer -->
    <tr>
      <td align="center" bgcolor="#e9ecef" style="padding: 24px;">
        <!--[if (gte mso 9)|(IE)]>
        <table align="center" border="0" cellpadding="0" cellspacing="0" width="600">
        <tr>
        <td align="center" valign="top" width="600">
        <![endif]-->
       
        <!--[if (gte mso 9)|(IE)]>
        </td>
        </tr>
        </table>
        <![endif]-->
      </td>
    </tr>
    <!-- end footer -->

  </table>
  <!-- end body -->

</body>
</html>
"""

translations = {
    "CustomMessage_SignUp": {
        "en": {
            "action_url": "{website}/confirm-user?email={encoded_email}&confirmation_code={####}",
            "title": "Confirm Your Email Address",
            "main_message": "Thanks for joining us! Your confirmation code is <span style=\"font-weight: bold;\">{####}</span>. You can copy and paste it in the verification user session. Alternatively, you can also tap the button below to confirm your email address.",
            "on_error_message": "If that doesn't work, copy and paste the following link in your browser.",
            "button_message": "Confirm!"
        },
        "es": {
            "action_url": "{website}/confirm-user?email={encoded_email}&confirmation_code={####}",
            "title": "Confirma tu email",
            "main_message": "¡Gracias por unirte a nosotros! Tu código de confirmación es {####}. Puedes copiarlo y pegarlo en la sesión de verificación de usuario. Alternativamente, también puedes tocar el botón de abajo para confirmar tu dirección de correo electrónico.",
            "on_error_message": "Si eso no funciona, copia y pega el siguiente enlace en tu navegador.",
            "button_message": "Confirmar!"
        },
        "fr": {
            "action_url": "{website}/confirm-user?email={encoded_email}&confirmation_code={####}",
            "title": "Confirmez votre adresse e-mail",
            "main_message": "Merci de vous joindre à nous ! Votre code de confirmation est {####}. Vous pouvez le copier et le coller dans la session de vérification de l'utilisateur. Alternativement, vous pouvez également appuyer sur le bouton ci-dessous pour confirmer votre adresse e-mail.",
            "on_error_message": "Si cela ne fonctionne pas, copiez et collez le lien suivant dans votre navigateur.",
            "button_message": "Confirmer!"
        }
    },
    "CustomMessage_ForgotPassword": {
        "en": {
            "action_url": "{website}/reset-password?email={encoded_email}&temporary_password={####}",
            "title": "Restart Password",
            "main_message": "Recently you have requested a password change, your temporary password is <span style=\"font-weight: bold;\">{####}</span>. Please go to the password reset section (click the button below) and paste your temporary password there",
            "on_error_message": "If that doesn't work, copy and paste the following link in your browser.",
            "button_message": "Go to reset!"
        },
        "es": {
            "action_url": "{website}/reset-password?email={encoded_email}&temporary_password={####}",
            "title": "Restablecer Contraseña",
            "main_message": "Recientemente has solicitado un cambio de contraseña, tu contraseña temporal es <span style=\"font-weight: bold;\">{####}</span>. Por favor, ve a la sección de restablecimiento de contraseña (haz clic en el botón de abajo) y pega tu contraseña temporal allí.",
            "on_error_message": "Si eso no funciona, copia y pega el siguiente enlace en tu navegador.",
            "button_message": "¡Ir al restablecimiento!"
        },
        "fr": {
            "action_url": "{website}/reset-password?email={encoded_email}&temporary_password={####}",
            "title": "Réinitialiser le Mot de Passe",
            "main_message": "Récemment, vous avez demandé un changement de mot de passe, votre mot de passe temporaire est <span style=\"font-weight: bold;\">{####}</span>. Veuillez vous rendre dans la section de réinitialisation du mot de passe (cliquez sur le bouton ci-dessous) et collez votre mot de passe temporaire là-bas.",
            "on_error_message": "Si cela ne fonctionne pas, copiez et collez le lien suivant dans votre navigateur.",
            "button_message": "Aller à la réinitialisation !"
        }
    }
}


def prepare_custom_email(event):
    trigger_source = event['triggerSource']
    request = event.get('request', {})
    email = request.get('userAttributes', {}).get('email')
    if trigger_source in translations and email:
        available_translations = translations[trigger_source]
        encoded_email = quote(email)
        lang = request.get('clientMetadata', {}).get('navigatorLanguaje', 
        'en').lower()[:2]
        values = available_translations[lang] if lang in available_translations else available_translations["en"]
        event['response']['emailSubject'] = values["title"].lower()
        final_html = html
        for key in values:
            final_html = final_html.replace("{%s}" % key, values[key])
        event['response']['emailMessage'] = final_html\
                                            .replace("{encoded_email}", encoded_email)\
                                            .replace("{website}", os.environ.get("site_url", ""))
    return event