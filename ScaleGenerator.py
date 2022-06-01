from keyidentifier import notes_mapping, KeyIdentifier, Chords
NUMBER_OF_FRETS = 20
key_dict = KeyIdentifier().generate_key_dict(return_numbers=True)


class ScaleGenerator:
    def __init__(self):
        self.chords_func = Chords()
        self.key_ident = KeyIdentifier()
        self.key_dict = self.key_ident.generate_key_dict(return_numbers=True)
        self.root_note_num = None
    def get_numeric_values_for_tuning(self, tuning=['E', 'A', 'D', 'G', 'B', 'E']):
        # standart tuning will be [4, 9, 2, 7, 11, 4]
        ch = Chords()
        tuning_num = list(map(ch.get_num_from_note, tuning))
        return tuning_num
    
    def generate_scale_for_one_string(self, root_note: str, string_note_num: int):
        # for ex. scale from root for C major is [0, 2, 4, 5, 7, 9, 11]
        scale_from_root = self.key_dict[root_note]
        # then scale_minus_string_num for C major for string E will be [0, 2, 4, 5, 7, 9, 11] - 4 for each element
        scale_minus_string_num = [scale_element - string_note_num for scale_element in scale_from_root]
        scale_for_string = set()
        for elem in scale_minus_string_num:
            while elem <= NUMBER_OF_FRETS:
                if elem >= 0:
                    scale_for_string.add(elem)
                elem += 12
        return scale_for_string
    
    def generate_scale_for_tuning(self, tuning_num, root_note: str):
        scale = []
        for string_note_num in tuning_num:
            string_scale = list(self.generate_scale_for_one_string(root_note, string_note_num))
            string_note = self.chords_func.get_note_from_num(string_note_num)
            scale.append((string_note, string_scale))
        return scale
    
    def draw_scale(self, scale, root_note=None):
        for string_name, scale_for_string in scale[::-1]:
            print('{} {}'.format(string_name, self.draw_string(scale_for_string, root_note)))
        scale_levels = [8, 7, 7, 7, 7, 10, 10]
        scale_marks = [1, 3, 5, 7, 9, 12, 15]
        scale_numbers = ''
        for level, mark in zip(scale_levels, scale_marks):
            scale_numbers = ''.join([scale_numbers, ' ' * level])
            scale_numbers = ''.join([scale_numbers, str(mark)])
        print(scale_numbers)
    
    def draw_string(self, scale_for_string, root_note=None):
        if root_note:
            root_note_num = self.chords_func.get_num_from_note(root_note)
        
        delim = '|'
        scale = ''
        for fret in range(NUMBER_OF_FRETS + 1):
            if fret in scale_for_string:
               # if fret % 12 == root_note_num:
                #    scale = delim.join([scale, ' • '])
                #else:
                scale = delim.join([scale, ' o '])
            else:
                scale = delim.join([scale, '   '])
        return scale