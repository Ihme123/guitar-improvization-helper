import re
# key_dict holds the information about notes in different keys
# in format <key>: [<notes for that key>]
notes_mapping = {
    'C': 0,
    'C#': 1,
    'D': 2,
    'D#': 3,
    'E': 4,
    'F': 5,
    'F#': 6,
    'G': 7,
    'G#': 8,
    'A': 9,
    'A#': 10,
    'B': 11
    }


class KeyIdentifier:
    def __init__(self, *args):
        self.chords_func = Chords()
        self.key_dict = self.generate_key_dict()
        
    def __call__(self, *chords):
        print(self.identify_the_key(*chords))
    
    def list_simularity(self, list1, list2):
        """Calculate the number of intersecting elements of two lists."""
        return len(set(list1) & set(list2))
    
    def notes_from_chords(self, *chords):
        """Get all the notes from a list of chords"""
        self.notes_of_song = set()
        for chord_name in chords:
            root_note, minor, seventh = self.chords_func.parse_chord_name(chord_name)
            notes_of_chord = self.chords_func.get_chord(root_note, minor, seventh)
            self.notes_of_song.update(notes_of_chord)
        return self.notes_of_song
    
    def calculate_most_probable_key(self, notes_of_song):
        """Calculate which key have the biggest number of given notes (notes_of_song)
        
        Also if most probable key is ambiguous (two keys have the same biggest probability), the function return both
            """
        most_probable_key, biggest_simularity = None, 0
        second_most_probable_key, second_biggest_simularity = None, 0
        for key, notes_of_the_key in self.key_dict.items():
            current_simularity = self.list_simularity(notes_of_the_key, notes_of_song)
            print('{} has {} of the same notes'.format(key, current_simularity))
            if current_simularity > biggest_simularity:
                second_most_probable_key, second_biggest_simularity = most_probable_key, biggest_simularity
                most_probable_key, biggest_simularity = key, current_simularity
        if second_biggest_simularity == biggest_simularity:
            return most_probable_key, second_most_probable_key
        return most_probable_key, None
    
    def identify_the_key(self, *chords):
        """Main function, giving the key of the song from some chords
        
        If key is ambiguous, return two most probable keys.
        """
        notes_of_song = self.notes_from_chords(*chords)
        most_probable_key, second_most_probable_key = self.calculate_most_probable_key(notes_of_song)
        if second_most_probable_key:
            return 'The song can be in  {} or {}. Enter more chords to find out more'.format(most_probable_key,
                                                                                             second_most_probable_key)
        else:
            return 'The key of the song is {}'.format(most_probable_key)
    
    def generate_key_dict(self, return_numbers=False):
        """Generate the dictionary with the notes for each key in keys"""
        keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 
                'F#', 'G', 'G#', 'A', 'A#', 'B']
        major = [0, 2, 4, 5, 7, 9, 11]
        key_dict_generated = {}
        for root_note in keys:
            root_num = self.chords_func.get_num_from_note(root_note)
            if return_numbers:
                key_dict_generated[root_note] = [(root_num + step) % 12 for step in major]
            else:
                key_dict_generated[root_note] = [self.chords_func.get_note_from_num((root_num + step) % 12) for step in major]
            #print('{} - {}'.format(root_note, key_dict_generated[root_note]))
        return key_dict_generated
        
class Chords:
    """Helper class"""
    def __init__(self):
        self.notes_mapping = notes_mapping
        
    def get_note_from_num(self, note_num: int):
        """Returns name of the note from it's number, according to notes_mapping
        
        for ex.: input: 4, output: 'E'.
        """
        # If note_num is greater then 11, then note_num is modulo of 12 + the 0th element, making the full circle 
        note_num_adj = note_num % 12
        keys_list = list(self.notes_mapping.keys())
        values_list = list(self.notes_mapping.values())
        return keys_list[values_list.index(note_num_adj)]
    
    def get_num_from_note(self, note):
        """Returns the number of the note according to notes_mapping"""
        return self.notes_mapping[note]
    
    def get_chord(self, note, minority=False, seventh=None):
        """One function for calling get_major or get_minor"""
        if minority:
            return self.get_minor(note, seventh)
        else:
            return self.get_major(note, seventh)
    
    def get_major(self, note, seventh=None):
        """Given the root note of the chord, return the notes in major chord"""
        root_note_num = self.get_num_from_note(note)
        # major_steps shows how many semitones we need to adjust the root note to get major chord
        major_steps = [0, 4, 7]
        if seventh:
            major_steps.append(10)
        chord_notes = [self.get_note_from_num(root_note_num + major_steps[i]) for i in range(len(major_steps))]
        return chord_notes
    
    def get_minor(self, note, seventh=None):
        """Given the root note of the chord, return the notes in minor chord"""
        root_note_num = self.get_num_from_note(note)
        # minor_steps shows how many semitones we need to adjust the root note to get minor chord
        minor_steps = [0, 3, 7]
        if seventh:
            minor_steps.append(10)
        chord_notes = [self.get_note_from_num(root_note_num + minor_steps[i]) for i in range(len(minor_steps))]
        return chord_notes
    
    def parse_chord_name(self, chord_name):
        """Return the root note, if the chord is minor (true/false) and if chord has a 7th postscript"""
        match = re.findall('^(\w#?)(m?)(7?)', chord_name)
        root_note, minor, seventh = match[0]
        majority = (minor == 'm')
        seventh = (seventh == '7')
        return root_note, minor, seventh