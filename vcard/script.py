import os
import datetime
import typer
from functools import wraps

DEFAULT_CONFIG_FILE = "config.conf"

class CustomTyper(typer.Typer):
    def __init__(self, *args, config_file="config.json", **kwargs):
        super().__init__(*args, **kwargs)
        self.config = {}
        self.config_file = config_file  # Accept the default config file as a parameter

    def __call__(self, *args, **kwargs):
        # Load the configuration file before running any command
        self.load_config()
        super().__call__(*args, **kwargs)

    def load_config(self):
        """Load the configuration file and parse settings."""
        config_path = self.config_file
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                for line in f:
                    # Skip empty lines and comments
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    # Parse the setting in the format `setting_name: value`
                    if "=" in line:
                        key, value = line.split("=", 1)
                        self.config[key.strip()] = value.strip()
            typer.secho(f"✅ Loaded configuration from {config_path}", fg=typer.colors.GREEN)
        else:
            typer.secho(f"⚠️  Configuration file not found: {config_path}", fg=typer.colors.YELLOW)

app = CustomTyper(config_file=os.path.join(os.path.dirname(__file__), DEFAULT_CONFIG_FILE), help="A CLI tool to generate RSS feeds from markdown files")

def generate_opml_from_vcards(vcard_files):
    """
    Reads vCard files and generates an OPML file.

    Args:
        vcard_files (list): List of paths to vCard files.
    """
    import vobject
    from opyml import OPML, Outline

    opml = OPML()

    for vcard_file in vcard_files:
        with open(vcard_file, "r", encoding="utf-8") as f:
            for vcard in vobject.readComponents(f):
                # Extract the name and feed URL from the vCard
                name = vcard.fn.value if hasattr(vcard, "fn") else "Unknown"
                feed_url = vcard.x_feed.value if hasattr(vcard, "x_feed") else None

                if feed_url:
                    opml.body.outlines.append(
                        Outline(text=name, title=name, xml_url=feed_url)
                    )

    return opml.to_xml()

def inject_settings(*settings):
    """
    A decorator to inject specific settings from the configuration file into the command.
    If a setting is not provided via the command arguments, it will be loaded from the configuration file.
    """
    def decorator(func):
        @wraps(func)  # Preserve the original function metadata
        def wrapper(*args, **kwargs):
            # Inject each requested setting
            for setting in settings:
                if setting not in kwargs or kwargs[setting] is None:
                    value = app.config.get(setting)
                    if value is None:
                        continue
                        # typer.secho(
                        #     f"❌ The '{setting}' parameter is not defined and cannot be loaded from the configuration file.",
                        #     fg=typer.colors.RED,
                        # )
                        # raise typer.Exit()
                    kwargs[setting] = value
            return func(*args, **kwargs)
        return wrapper
    return decorator
    
@app.command()
@inject_settings("directory")
def connections(
    directory: str = typer.Option(None, help="Directory to retrieve the vCards (.vcf or .vcard files)"),
    output: str = typer.Option(None, help="Output OPML file"),
):   
    if not directory:
        directory = typer.prompt("📁 Enter the directory to retrieve the vCards (.vcf or .vcard files)")

    if not os.path.isdir(directory):
        typer.secho(f"❌ The specified directory does not exist: {directory}", fg=typer.colors.RED)
        raise typer.Exit()

    directory = os.path.abspath(directory)

    files = [
        os.path.join(root, f)
        for root, _, files in os.walk(directory)
        for f in files
        if f.endswith(".vcf") or f.endswith(".vcard")
    ]

    opml = generate_opml_from_vcards(files)

    # Write the OPML to the output file
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(opml)

        typer.secho(f"✅ OPML file generated: {output}")
    else:
        print(opml)


vcard_main_attributes = {
    "fn": {"default": "", "description": "Full Name (FN)"},
    "n": {"default": "", "description": "Name (N) in the format LastName;FirstName"},
    "nickname": {"default": "", "description": "Nickname (NICKNAME)"},
    "lang": {"default": "en-US", "description": "Language (LANG) in the format 'language-region' (e.g., 'en-US', 'es-ES')"},
    "gender": {"default": "", "description": "Gender (GENDER), e.g., 'M' for Male, 'F' for Female, or 'O' for Other"},
    "email": {"default": "", "description": "Email (EMAIL), e.g., 'example@mail.com'"},
    "categories": {"default": "", "description": "Categories (comma-separated, CATEGORIES), e.g., 'gamer,programmer'"},
    "bday": {"default": "", "description": "Birthday (BDAY) in the format YYYY-MM-DD"},
    "anniversary": {"default": "", "description": "Anniversary date (ANNIVERSARY) in the format YYYY-MM-DD"},
    "kind": {"default": "individual", "description": "Type of entity (KIND), e.g., 'individual' or 'org'"},
    "adr": {"default": "", "description": "Address (ADR) in the format ';;Street;City;State;PostalCode;Country'"},
    "tel": {"default": "", "description": "Telephone number (TEL), e.g., '+1234567890'"},
    "impp": {"default": "", "description": "Instant messaging protocol (IMPP), e.g., 'aim:exampleuser'"},
    "photo": {"default": "", "description": "URL to a photo (PHOTO), e.g., 'http://example.com/photo.jpg'"},
    "note": {"default": "", "description": "A short description about you (NOTE)"},
    "url": {"default": "", "description": "URL to public profile or personal web (URL), e.g., 'https://my.web.example.com/profile'"},
    "source": {"default": None, "description": "URL where the vCard will be hosted or can found (SOURCE)"},
}


@app.command()
def create(
    output: str = typer.Option("output.vcf", help="Output file to save the vCard"),
    interactive: bool = typer.Option(True, help="Interactive prompts"),
    fn: str = typer.Option(vcard_main_attributes["fn"]["default"], help=vcard_main_attributes["fn"]["description"]),
    n: str = typer.Option(vcard_main_attributes["n"]["default"], help=vcard_main_attributes["n"]["description"]),
    nickname: str = typer.Option(vcard_main_attributes["nickname"]["default"], help=vcard_main_attributes["nickname"]["description"]),
    lang: str = typer.Option(vcard_main_attributes["lang"]["default"], help=vcard_main_attributes["lang"]["description"]),
    gender: str = typer.Option(vcard_main_attributes["gender"]["default"], help=vcard_main_attributes["gender"]["description"]),
    email: str = typer.Option(vcard_main_attributes["email"]["default"], help=vcard_main_attributes["email"]["description"]),
    categories: str = typer.Option(vcard_main_attributes["categories"]["default"], help=vcard_main_attributes["categories"]["description"]),
    note: str = typer.Option(vcard_main_attributes["note"]["default"], help=vcard_main_attributes["note"]["description"]),
    url: str = typer.Option(vcard_main_attributes["url"]["default"], help=vcard_main_attributes["url"]["description"]),
    source: str = typer.Option(vcard_main_attributes["source"]["default"], help=vcard_main_attributes["source"]["description"]),
    bday: str = typer.Option(vcard_main_attributes["bday"]["default"], help=vcard_main_attributes["bday"]["description"]),
    anniversary: str = typer.Option(vcard_main_attributes["anniversary"]["default"], help=vcard_main_attributes["anniversary"]["description"]),
    kind: str = typer.Option(vcard_main_attributes["kind"]["default"], help=vcard_main_attributes["kind"]["description"]),
    adr: str = typer.Option(vcard_main_attributes["adr"]["default"], help=vcard_main_attributes["adr"]["description"]),
    tel: str = typer.Option(vcard_main_attributes["tel"]["default"], help=vcard_main_attributes["tel"]["description"]),
    impp: str = typer.Option(vcard_main_attributes["impp"]["default"], help=vcard_main_attributes["impp"]["description"]),
    photo: str = typer.Option(vcard_main_attributes["photo"]["default"], help=vcard_main_attributes["photo"]["description"]),
):
    """
    Generate a vCard by asking the user for information.
    """

    custom_attributes = {}
    # Prompt the user for vCard fields if interactive mode is enabled
    if interactive:
        typer.secho("Let's create a new vCard!", fg=typer.colors.CYAN)
        temp_file = "vcard_create.tmp"

        # Load existing data from the temp file if it exists
        temp_data = {}
        if os.path.exists(temp_file):
            with open(temp_file, "r", encoding="utf-8") as f:
                for line in f:
                    key, value = line.strip().split("=", 1)
                    temp_data[key] = value

        def save_entry_temp(key, value):
            """Save a single entry to the temp file."""
            temp_data[key] = value
            with open(temp_file, "w", encoding="utf-8") as f:
                for k, v in temp_data.items():
                    f.write(f"{k}={v}\n")

        def prompt_with_temp(key, description, default):
            """Prompt the user and save the value to the temp file."""
            value = typer.prompt(description, default=temp_data.get(key, default))
            save_entry_temp(key, value)
            return value

        fn = prompt_with_temp("fn", vcard_main_attributes["fn"]["description"], fn)
        n = prompt_with_temp("n", vcard_main_attributes["n"]["description"], n)
        nickname = prompt_with_temp("nickname", vcard_main_attributes["nickname"]["description"], nickname)
        lang = prompt_with_temp("lang", vcard_main_attributes["lang"]["description"], lang)
        gender = prompt_with_temp("gender", vcard_main_attributes["gender"]["description"], gender)
        email = prompt_with_temp("email", vcard_main_attributes["email"]["description"], email)
        categories = prompt_with_temp("categories", vcard_main_attributes["categories"]["description"], categories)
        bday = prompt_with_temp("bday", vcard_main_attributes["bday"]["description"], bday)
        anniversary = prompt_with_temp("anniversary", vcard_main_attributes["anniversary"]["description"], anniversary)
        kind = prompt_with_temp("kind", vcard_main_attributes["kind"]["description"], kind)
        adr = prompt_with_temp("adr", vcard_main_attributes["adr"]["description"], adr)
        tel = prompt_with_temp("tel", vcard_main_attributes["tel"]["description"], tel)
        impp = prompt_with_temp("impp", vcard_main_attributes["impp"]["description"], impp)
        photo = prompt_with_temp("photo", vcard_main_attributes["photo"]["description"], photo)
        note = prompt_with_temp("note", vcard_main_attributes["note"]["description"], note)
        url = prompt_with_temp("url", vcard_main_attributes["url"]["description"], url)
        source = prompt_with_temp("source", vcard_main_attributes["source"]["description"], source)

        # Add the X-FEED attribute if the user wants to include it
        add_feed = typer.confirm("Do you want to add an X-FEED attribute for an RSS feed?", default=False)
        if add_feed:
            feed_url = prompt_with_temp("x_feed", "Enter the RSS feed URL", "")
            custom_attributes["X-FEED"] = feed_url

        typer.secho("ℹ️ If you have feeds in different languages, add X-FEED;LANGUAGE:language-region to the vCard.", fg=typer.colors.BLUE)
        custom_feeds = []
        add_feed = typer.confirm("Do you want to add custom X-FEED;LANGUAGE:language-region entries?", default=False)

        while add_feed:
            language = prompt_with_temp(
                f"x_feed_language_{len(custom_feeds)}",
                "Enter the language-region (e.g., 'en-US', 'es-ES')",
                ""
            ).strip()
            feed_url = prompt_with_temp(
                f"x_feed_url_{len(custom_feeds)}",
                "Enter the feed URL",
                ""
            ).strip()
            custom_feeds.append((language, feed_url))
            add_feed = typer.confirm("Do you want to add another X-FEED;LANGUAGE entry?", default=False)

        # Add the X-FEED;LANGUAGE entries to the vCard content
        for language, feed_url in custom_feeds:
            attribute_name = f"FEED;LANGUAGE={language}"
            custom_attributes[f"X-{attribute_name}"] = feed_url
    
        add_custom = typer.confirm("Do you want to add custom attributes for social media links or other information?", default=False)

        # Custom attributes for social media links or other information
        while add_custom:
            attribute_name = typer.prompt("Enter the name of the custom attribute (it will be prefixed with 'X-')").strip().upper()
            # Prompt the user for the custom attribute value and save it to the temp file
            attribute_value = prompt_with_temp(
                f"x_{attribute_name}",
                f"Enter the value for X-{attribute_name}",
                ""
            )
            custom_attributes[f"X-{attribute_name}"] = attribute_value
            add_custom = typer.confirm("Do you want to add another custom attribute?", default=False)

    # Generate the vCard content
    # Start building the vCard content
    vcard_content = "BEGIN:VCARD\nVERSION:4.0\n"

    # Add optional fields conditionally
    if fn:
        vcard_content += f"FN:{fn}\n"
    if n:
        vcard_content += f"N:{n};;;;\n"
    if nickname:
        vcard_content += f"NICKNAME:{nickname}\n"
    if lang:
        vcard_content += f"LANG:{lang}\n"
    if gender:
        vcard_content += f"GENDER:{gender}\n"
    if email:
        vcard_content += f"EMAIL:{email}\n"
    if categories:
        vcard_content += f"CATEGORIES:{categories}\n"
     if bday:
        vcard_content += f"BDAY:{bday}\n"
    if anniversary:
        vcard_content += f"ANNIVERSARY:{anniversary}\n"
    if kind:
        vcard_content += f"KIND:{kind}\n"
    if adr:
        vcard_content += f"ADR:{adr}\n"
    if tel:
        vcard_content += f"TEL:{tel}\n"
    if impp:
        vcard_content += f"IMPP:{impp}\n"
    if photo:
        vcard_content += f"PHOTO:{photo}\n"
    if note:
        vcard_content += f"NOTE;LANGUAGE=en-US:{note}\n"
    if url:
        vcard_content += f"URL:{url}\n"
    if source:
        vcard_content += f"SOURCE:{source}\n"
   

    # Add custom attributes conditionally
    for attribute_name, attribute_value in custom_attributes.items():
        vcard_content += f"{attribute_name}:{attribute_value}\n"

    # End the vCard content
    vcard_content += "END:VCARD"

    # Print a summary of the vCard
    typer.secho("\nSummary of the vCard:", fg=typer.colors.CYAN)
    typer.echo(vcard_content)
    typer.echo("\n")

    # Ask for confirmation before saving
    if interactive:
        confirm_save = typer.confirm("Do you want to save this vCard to the file?", default=True)
        if not confirm_save:
            typer.secho("❌ Operation canceled. The vCard was not saved.", fg=typer.colors.RED)
            raise typer.Exit()

    # Write the vCard to the output file
    with open(output, "w", encoding="utf-8") as f:
        f.write(vcard_content)

    typer.secho(f"✅ vCard generated and saved to {output}", fg=typer.colors.GREEN)

if __name__ == "__main__":
    app()

