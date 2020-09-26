export default function (lowest, highest, marks_list) {

    for (let i = 0; i < marks_list.length; i++) {
        if (marks_list[i] > highest || marks_list[i] < lowest) {
            alert("Invalid Mark");
            return false;
        }
    }
    return true;

}