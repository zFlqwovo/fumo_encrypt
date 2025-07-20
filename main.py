import base64
import re
import sys

Base64_List = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

Fumo_List = [
    'fumo-', 'Fumo-', 'fUmo-', 'fuMo-', 'fumO-', 'FUmo-', 'FuMo-', 'FumO-', 'fUMo-', 'fUmO-', 'fuMO-', 'FUMo-', 'FUmO-', 'fUMO-', 'FUMO-',
    'fumo.', 'Fumo.', 'fUmo.', 'fuMo.', 'fumO.', 'FUmo.', 'FuMo.', 'FumO.', 'fUMo.', 'fUmO.', 'fuMO.', 'FUMo.', 'FUmO.', 'fUMO.', 'FUMO-',
    'fumo,', 'Fumo,', 'fUmo,', 'fuMo,', 'fumO,', 'FUmo,', 'FuMo,', 'FumO,', 'fUMo,', 'fUmO,', 'fuMO,', 'FUMo,', 'FuMO,', 'fUMO,', 'FUMO-',
    'fumo+', 'Fumo+', 'fUmo+', 'fuMo+', 'fumO+', 'FUmo+', 'FuMo+', 'FumO+', 'fUMo+', 'fUmO+', 'fuMO+', 'FUMO+',
    'fumo|', 'Fumo|', 'fUmo|', 'fuMo|', 'fumO|', 'FUmo|', 'FuMo|', 'FumO|', 'fUMo|', 'fUmO|', 'fuMO|', 'FUMo|', 'FUmO|', 'fUMO-',
    'fumo/', 'Fumo/', 'fUmo/'
]

Fumo_Chars = list(dict.fromkeys(Fumo_List))[:64]

Encode_Map = {b64_char: fumo_char for b64_char, fumo_char in zip(Base64_List, Fumo_List)}
Decode_Map = {fumo_char: b64_char for b64_char, fumo_char in zip(Base64_List, Fumo_List)}

def fumo_encrypt(text: str) -> str:
    try:
        text_bytes = text.encode('utf-8')
        base64_bytes = base64.b64encode(text_bytes)
        base64_string = base64_bytes.decode('utf-8')

        base64_body = base64_string.rstrip('=')
        padding = len(base64_string) - len(base64_body)

        fumo_body = ''.join([Encode_Map[char] for char in base64_body])
        
        return fumo_body + '=' * padding
    except Exception as e:
        return f"加密出错: {e}"

def fumo_decrypt(fumo_text: str) -> str:
    try:
        fumo_body = fumo_text.rstrip('=')
        padding_count = len(fumo_text) - len(fumo_body)
        
        fumo_words = re.findall(r'(\w+[-.,+|/])', fumo_body)
        
        if ''.join(fumo_words) != fumo_body:
            return "解密失败: 包含无效的 Fumo 字符或格式错误。"

        base64_body = ''.join([Decode_Map[word] for word in fumo_words])

        base64_string = base64_body + '=' * padding_count
        
        decoded_bytes = base64.b64decode(base64_string)
        original_text = decoded_bytes.decode('utf-8')
        return original_text
    except (KeyError, IndexError):
        return "解密失败: 包含无效的 Fumo 字符。"
    except Exception as e:
        return f"解密失败: {e}"

def main():
    print("--- Fumo 语加密/解密工具 ---")
    while True:
        print("请选择操作:")
        print("   1. 加密文本")
        print("   2. 解密 Fumo")
        print("   3. 退出程序")
        
        choice = input("请输入选项 (1, 2, 3): ")
        
        if choice == '1':
            text_to_encrypt = input("请输入要加密的原文: \n")
            encrypted = fumo_encrypt(text_to_encrypt)
            print("\n--- 加密结果 ---")
            print(encrypted)
            print("------------------")
            
        elif choice == '2':
            text_to_decrypt = input("请输入要解密的 Fumo 语: \n")
            decrypted = fumo_decrypt(text_to_decrypt)
            print("\n--- 解密结果 ---")
            print(decrypted)
            print("------------------")

        elif choice == '3':
            print("fumo~")
            sys.exit()
            
        else:
            print("这不是个有效的选项哦。请选 1、2 或 3 吧，fumo~！")

if __name__ == "__main__":
    main()