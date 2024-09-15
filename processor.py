from datetime import datetime, timedelta
from state import State
from reader import file_input

def process_nem12_file(file):
    current_nmi = None
    interval_length = None
    values = []
    query_list = []
    line_count = 0
    state = State.START

    try:
        for row in file_input(file):
            line_count += 1
            match state:
                case State.START:
                    if row[0] == '100':
                        state = State.ROW_100
                    else:
                        raise ValueError(f"Unexpected row type on line {line_count}: Actual row: {row[0]}. Expected: 100")
                case State.ROW_100:
                    if row[0] == '200':
                        state = State.ROW_200
                        current_nmi = row[1]
                        interval_length = int(row[8])
                    else:
                        raise ValueError(f"Unexpected row type on line {line_count}: Actual row: {row[0]}. Expected: 200")
                case State.ROW_200:
                    if row[0] == '300':
                        state = State.ROW_300
                        consumption_values = row[2:50]
                        timestamp = datetime.strptime(row[1], '%Y%m%d')
                        for consumption in consumption_values:
                            values.append(f"('{current_nmi}', '{timestamp.strftime('%Y-%m-%d %H:%M:%S')}', {consumption})")
                            timestamp += timedelta(minutes=interval_length)
                    else:
                        raise ValueError(f"Unexpected row type on line {line_count}: Actual row: {row[0]}. Expected: 300")
                case State.ROW_300:
                    match row[0]:
                        case '300':
                            state = State.ROW_300
                            consumption_values = row[2:50]
                            timestamp = datetime.strptime(row[1], '%Y%m%d')
                            for consumption in consumption_values:
                                values.append(f"('{current_nmi}', '{timestamp.strftime('%Y-%m-%d %H:%M:%S')}', {consumption})")
                                timestamp += timedelta(minutes=interval_length)
                        case '200':
                            state = State.ROW_200
                            if current_nmi and values:
                                query_list.append(f"INSERT INTO meter_readings (nmi, timestamp, consumption) VALUES {', '.join(values)};")
                                values = []
                            current_nmi = row[1]
                            interval_length = int(row[8])
                        case '900':
                            state = State.ROW_900
                            if current_nmi and values:
                                query_list.append(f"INSERT INTO meter_readings (nmi, timestamp, consumption) VALUES {', '.join(values)};")
                        # 400 and 500 are ignored due to unnecessary data. This may result in uniquely malformed files being parsed anyway.
                        # To maintain readability and simplicity, I have chosen to ignore these cases in current state.
                        case '400' | '500':
                            continue
                        case _:
                            raise ValueError(f"Unexpected row type on line {line_count}: Actual row: {row[0]}. Expected: 200, 300, 400, 500, or 900")
                case _:
                    if State.ROW_900:
                        raise ValueError(f"Malformed file. There is data present after expected end of file on line {line_count}")
                    else:
                        expected_value = {
                            State.START: '100',
                            State.ROW_100: '200',
                            State.ROW_200: '300',
                            State.ROW_300: '200, 300, 400, 500, or 900',
                        }.get(state)
                        raise ValueError(f"Unexpected row type on line {line_count}: Actual row: {row[0]}. Expected: {expected_value}")

    except IndexError as e:
        raise ValueError(f"IndexError on line {line_count}: {str(e)}")
    
    if state != State.ROW_900:
        raise ValueError(f"Malformed file. Final row should be: 900. Actual row type: {row[0]}")

    return query_list
