# Use Musescore to load and export as Midi
# Use "http://flashmusicgames.com/midi/mid2txt.php" to convert Midi to Text
# Input file is "text.txt"
# Output file is "output.chart"

def main():
    with open('test.txt') as f:
        lines = f.readlines()

    notes = []
    temp_changes = []

    for i in range(0, len(lines)):
        line = lines[i]

        parts = line.split(' ')

        if len(parts) >= 3:
            if parts[1] == 'Tempo':
                temp_changes.append({
                    'time': parts[0],
                    'speed': parts[2][:len(parts[2]) - 1]
                })
            elif parts[1] == 'On' and parts[4] != 'v=0\n':
                time = parts[0]
                note = parts[3][2:]
                channel = parts[2][3:]
                length = get_note_length(lines[i + 1:], note, channel, int(time))

                notes.append({
                    'time': time,
                    'note': note,
                    'channel': channel,
                    'length': length
                })

    create_chart(temp_changes, notes)


def get_note_length(lines, note, channel, time):
    for line in lines:
        parts = line.split(' ')

        if len(parts) > 2 and parts[1] == 'On' and parts[3][2:] == note and parts[2][3:] == channel:
            return str(int(parts[0]) - time)

    return 0


def create_chart(temp_changes, notes):
    a = """[Song]
{
  Name = "Midi to Chart Song"
  Offset = 0
  Resolution = 192
  Player2 = bass
  Difficulty = 0
  PreviewStart = 0
  PreviewEnd = 0
  Genre = "rock"
  MediaType = "cd"
}
[SyncTrack]
{
  0 = TS 4
"""
    b = """}
[Events]
{
}
"""

    tempo_lines = []

    for tempo in temp_changes:
        time = str(int(int(tempo['time']) / 2.5))
        percentage = 600000.0 / int(tempo['speed'])
        speed = str(int(percentage * 100000))
        line = time + ' = B ' + speed + '\n'
        tempo_lines.append(line)

    track_names = [
        'ExpertSingle',
        'ExpertDoubleGuitar',
        'ExpertDoubleBass',
        'ExpertDoubleRhythm',
        'ExpertKeyboard',
        'HardSingle',
        'HardDoubleGuitar',
        'HardDoubleBass',
        'HardDoubleRhythm',
        'HardKeyboard',
        'MediumSingle',
        'MediumDoubleGuitar',
        'MediumDoubleBass',
        'MediumDoubleRhythm',
        'MediumKeyboard'
    ]

    tracks = {
        'ExpertSingle': [],
        'ExpertDoubleGuitar': [],
        'ExpertDoubleBass': [],
        'ExpertDoubleRhythm': [],
        'ExpertKeyboard': [],
        'HardSingle': [],
        'HardDoubleGuitar': [],
        'HardDoubleBass': [],
        'HardDoubleRhythm': [],
        'HardKeyboard': [],
        'MediumSingle': [],
        'MediumDoubleGuitar': [],
        'MediumDoubleBass': [],
        'MediumDoubleRhythm': [],
        'MediumKeyboard': []
    }

    note_shrink_percentage = 0.8
    note_length_cut_off = 500

    for note in notes:
        if 0 <= int(note['channel']) - 1 < len(track_names):
            button = int(note['note']) % 5
            time = str(int(int(note['time']) / 2.5))

            actual_length = int(note['length']) / 2.5
            adjusted_length = actual_length * note_shrink_percentage
            if adjusted_length <= note_length_cut_off:
                adjusted_length = 0
            else:
                adjusted_length = int(adjusted_length)
            length = str(adjusted_length)

            line = time + ' = N ' + str(button) + ' ' + length + '\n'
            track_name = track_names[int(note['channel']) - 1]
            tracks[track_name].append(line)

    with open('output.chart', 'w') as f:
        f.write(a)
        f.writelines(tempo_lines)
        f.write(b)

        for track_name in tracks:
            f.write('[' + track_name + ']\n{\n')
            f.writelines(tracks[track_name])
            f.write('}\n')


if __name__ == '__main__':
    main()
