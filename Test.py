import yaml
import pandas as pd

KEY_CONFIG_TRANSLATION_FILE_PATH = "translationFile"
KEY_CONFIG_SUPPORTED_LANGUAGES = "languages"
KEY_CONFIG_VARIABLE_NAME = "variableName"
KEY_CONFIG_LOCALE = "locale"
KEY_CONFIG_STRINGS_PATH = "stringsPath"
KEY_CONFIG_XML_PATH = "xmlPath"
KEY_CONFIG_OUTPUT_PATH = "outputFile"

config = yaml.safe_load(open("config.yaml"))
dataframe = pd.read_csv(f"{config[KEY_CONFIG_TRANSLATION_FILE_PATH]}", delimiter=";")
print(dataframe.head())
print()


def create_ios_string_mapping(key, value):
    return f"\"{key}\" = \"{value}\";"


def create_android_string_mapping(key, value):
    return f"    <string name=\"{key}\">{value}</string>"


def remove_none_values(value_list):
    return [i for i in value_list if i is not None]


def get_language_details(language):
    # This part is required, as the language string, f.e 'Dutch-NL' is 1 layer higher than the required data
    current_language_key = list(language.keys())[0]
    language = language[current_language_key]

    string_path = language[KEY_CONFIG_STRINGS_PATH]
    xml_path = language[KEY_CONFIG_XML_PATH]

    if xml_path is None and string_path is None:
        pass
    else:
        return language


def get_languages():
    language_list = [get_language_details(x) for x in config[KEY_CONFIG_SUPPORTED_LANGUAGES]]
    return remove_none_values(language_list)


def generate_language_resource_files(language):
    locale = language[KEY_CONFIG_LOCALE]
    string_path = language[KEY_CONFIG_STRINGS_PATH]
    xml_path = language[KEY_CONFIG_XML_PATH]

    keys_df = dataframe[config[KEY_CONFIG_VARIABLE_NAME]]
    # print(keys_df.head())

    if string_path is not None:
        f = open(string_path, "w")

        results = [create_ios_string_mapping(x, y) for x, y in
                   zip(dataframe[config[KEY_CONFIG_VARIABLE_NAME]], dataframe[locale])]

        [f.write(f"{x}\n") for x in results]

        f.close()

    if xml_path is not None:
        f = open(xml_path, "w")
        f.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
        f.write("<resources>\n")

        results = [create_android_string_mapping(x, y) for x, y in
                   zip(dataframe[config[KEY_CONFIG_VARIABLE_NAME]], dataframe[locale])]
        [f.write(f"{x}\n") for x in results]

        f.write("</resources>")


def generate_dataframe_from_list(data, locale):
    return pd.DataFrame(data=data, columns=['Key', locale])


def generate_csv_from_resource_files(languages):
    t = [['yes', 'ja'], ['no', 'nein'], ['Greeting', 'Hello']]
    t2 = [['yes', 'oui'], ['no', 'non']]
    t3 = [['yes', 'ja'], ['no', 'nee']]

    df_1 = pd.DataFrame(data=t, columns=['Key', 'de-DE'])
    df_2 = pd.DataFrame(data=t2, columns=['Key', 'fr-FR'])
    df_3 = pd.DataFrame(data=t3, columns=['Key', 'nl-NL'])

    dfs = [df_1, df_2, df_3]
    final_pd = pd.DataFrame(data=[], columns=['Key'])

    for x in dfs:
        final_pd = pd.merge(left=final_pd, right=x, on='Key', how='outer')

    final_pd.to_csv(config[KEY_CONFIG_OUTPUT_PATH], index=False, sep=';', encoding='utf-8')
    print("Generated csv!")


result = get_languages()
[generate_language_resource_files(x) for x in result]

generate_csv_from_resource_files(result)
