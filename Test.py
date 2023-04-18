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


def ios_get_key_value_from_line(line):
    # Remove potential whitespaces at the start/end of the string
    modified_string = line.strip()

    # Remove the last character: "Yes" = "Ja"; -> "Yes" = "Ja"
    modified_string = modified_string[:-1]

    # Split the string to key/value: "Yes" = "Ja" -> ['"Yes" ', ' "Ja"']
    modified_string = modified_string.split('=')

    # Remove the first and last values of the key
    key = modified_string[0].strip()

    # The key can not contain '=', thus the value contains a combination of all possible entries
    value = ''.join(modified_string[1:]).strip()

    # Remove the first & last characters ('"'): "Yes" -> Yes & "No" -> No
    key = key[1:-1]
    value = value[1:-1]

    return [[key, value]]


def generate_csv_from_resource_files(languages):
    final_pd = pd.DataFrame(data=[], columns=['Key'])

    for current_language in languages:
        if current_language[KEY_CONFIG_STRINGS_PATH] is not None:
            key_list = []

            f = open(current_language[KEY_CONFIG_STRINGS_PATH], 'r')

            for line in f.readlines():
                key_list += ios_get_key_value_from_line(line)

            # Transform the key/value list to a dataframe, and merge it into the 'main' dataframe
            df = pd.DataFrame(data=key_list, columns=['Key', current_language[KEY_CONFIG_LOCALE]])
            final_pd = pd.merge(left=final_pd, right=df, on='Key', how='outer')
        if current_language[KEY_CONFIG_XML_PATH] is not None:
            print('xml path was not null!')

    final_pd.to_csv(config[KEY_CONFIG_OUTPUT_PATH], index=False, sep=';', encoding='utf-8')
    print("Generated csv!")


result = get_languages()
# [generate_language_resource_files(x) for x in result]

generate_csv_from_resource_files(result)
