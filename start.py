from huffman_alg import HuffmanCoding
import sys

def ask_user_compress_or_decompress():
    print('Вы хотите архивировать или разорхивировать файлы?')
    print('0 - архивировать')
    print('1 - разорхивировать')
    compress = input()
    if (compress == '0'):
        return True
    return False

def ask_user_password():
    print('Введите пароль на создаваемый архив (-1, если без пароля):', end=' ')
    password = input()
    return password

def get_input_files():
    print('Введите количество архивируемых файлов:', end=' ')
    files_cnt = int(input())
    files_paths = []
    for i in range(files_cnt):
        print('Введите путь к файлу ' + str(i) + ':', end=' ')
        files_paths.append(input())
    return files_paths

def create_archive_info_txt(file_paths, password):
    with open('archive_info.txt', 'w') as f:
        f.write(password + '\n' + str(len(file_paths)) + '\n')
        for i in file_paths:
            f.write(i + '\n')
    archive_info_file_huffman = HuffmanCoding('archive_info.txt')
    archive_info_file_huffman.compress()
    create_reverse_mapping_for_file(archive_info_file_huffman)

def create_reverse_mapping_for_file(huffman):
    with open(huffman.path.split('.')[0] + '_mapping.txt', 'w') as file:
        for code in huffman.reverse_mapping:
            file.write(code + ' ' + huffman.reverse_mapping[code] + '\n')
def compress_files():
    file_paths = get_input_files()
    password = ask_user_password()

    create_archive_info_txt(file_paths, password)

    for file in file_paths:
        huffman = HuffmanCoding(file)
        huffman.compress()
        create_reverse_mapping_for_file(huffman)

def ask_user_archive_info_file_location():
    print('Введите расположение сжатого файла с информацией об архиве:', end=' ')
    return input()

def fill_reverse_mapping_for_file(huffman, mapping_file):
    with open(mapping_file, 'r') as file:
        text = file.read()
        for code in text.split('\n'):
            if code == '':
                continue
            if len(code.split()) == 1:
                huffman.reverse_mapping[code.split()[0]] = '\n'
                continue
            huffman.reverse_mapping[code.split()[0]] = code.split()[1]
    return huffman

def check_password(password):
    print("Введите пароль от архива (-1, если его нет):", end=' ')
    return input() == password
def decompress_files():
    archive_info_compressed_location = ask_user_archive_info_file_location()

    archive_info_file_huffman = HuffmanCoding(archive_info_compressed_location)
    archive_info_file_huffman = fill_reverse_mapping_for_file(archive_info_file_huffman, archive_info_compressed_location[:-len('compressed.bin')] + 'mapping.txt')
    archive_info_file_huffman.decompress(archive_info_compressed_location)
    print(archive_info_file_huffman.path[:-len('compressed.bin')])
    with open(archive_info_file_huffman.path[:-len('compressed.bin')] + 'decompressed.txt', 'r+') as archive_info_file:
        text=archive_info_file.read()
        files_cnt = text.split('\n')[1]
        archive_password = text.split('\n')[0]
        if check_password(archive_password):
            files = text.split('\n')[2:]
            print('Файлы в архиве:')
            for file in files:
                print(file.split('\\')[-1])
            for file_location in files:
                file_huffman = HuffmanCoding(file_location)
                fill_reverse_mapping_for_file(file_huffman, file_location[:-len('.txt')] + '_mapping.txt')
                file_huffman.decompress(file_location[:-len('.txt')] + '_compressed.bin')
        else:
            print('!!!!НЕВЕРНЫЙ ПАРОЛЬ!!!!')



if ask_user_compress_or_decompress():
    compress_files()
else:
    decompress_files()


#output_path = h.compress()
#print("Compressed file path: " + output_path)

#decom_path = h.decompress(output_path)
#print("Decompressed file path: " + decom_path)