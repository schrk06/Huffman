import huffman as huf
import bintree_prettyprint as dra

a = "nekni_nettiri_jsmb_dayi"
d = huf.build_Huffman_tree(huf.build_frequency_list(a))
e = huf.encode_data(d, a)

print(e)  # Affiche les données compressées en binaire
print(huf.decode_data(d, e))  # Vérifie que le décodage fonctionne bien
h,q = huf.to_binary(e)  # Affiche la conversion binaire
print(huf.from_binary(h,q))