const newGrid = (size) => {
    let arr = new Array(size);

    for (let i = 0; i < size; i++) {
        arr[i] = new Array(size);
    }

    for (let i = 0; i < Math.pow(size, 2); i++) {
        arr[Math.floor(i/size)][i % size] = CONSTANT.UNASSIGNED;
    }

    return arr;    
}

// check for duplicates in col
const isColSafe = (grid, col, value) => {
    for (let row = 0; row < CONSTANT.GRID_SIZE; row++) {
        if (grid[row][col] === value) return false
    }
    return true;   
}

// check for duplicates in row
const isRowSafe = (grid, row, value) => {
    for (let col = 0; col < CONSTANT.GRID_SIZE; col++) {
        if (grid[row][col] === value) return false
    }
    return true;   
}

// check if box is good 
const isBoxSafe = (grid, box_row, box_col, value) => {
    for (let row = 0; row < CONSTANT.BOX_SIZE; row++) {
        for (let col = 0; col < CONSTANT.BOX_SIZE; col++) {
            if (grid[row + box_row][col + box_col] === value) return false;            
        }
    }
    return true;
}

const isSafe = (grid, row, col, value) => {
    return isColSafe(grid, col, value) && isRowSafe(grid, row, value) 
    && isBoxSafe(grid, row - row%3, col - col%3, value) && value !== CONSTANT.UNASSIGNED;
}

const findUnassignedPos = (grid, pos) => {
    for (let row = 0; row < CONSTANT.GRID_SIZE; row++) {
        for (let col = 0; col < CONSTANT.GRID_SIZE; col++) {
            if (grid[row][col] === CONSTANT.UNASSIGNED) {
                pos.row = row; 
                pos.col = col;
                return true;
            }
        }
    }
    return false;
}

const shuffleArray = (arr) => {
    let currIndex = arr.length;

    while (currIndex !== 0) {
        let randIndex = Math.floor(Math.random() * currIndex);
        currIndex -= 1;
        let temp = arr[currIndex];
        arr[currIndex] = arr[randIndex]
        arr[randIndex] = temp
    }

    return arr;
}

const isGridFull = (grid) => {
    return grid.every((row, i) => {
        return row.every((value, j) => {
            return value !== CONSTANT.UNASSIGNED;
        });
    });
}

const sudokuCreate = (grid) => {
    let unassigned_pos = {
        row: -1, 
        col: -1
    }

    if (!findUnassignedPos(grid, unassigned_pos)) return true;

    let number_list = shuffleArray([...CONSTANT.NUMBERS]);

    let row = unassigned_pos.row;
    let col = unassigned_pos.col;

    number_list.forEach((num, i) => {
        if (isSafe(grid, row, col, num)) {
            grid[row][col] = num;

            if(isGridFull(grid)) {
                return true;
            } else {
                if (sudokuCreate(grid)) {
                    return true;
                }
            }

            grid[row][col] = CONSTANT.UNASSIGNED;
        }
    });

    return isGridFull(grid);
}

const sudokuCheck = (grid) => {
    let unassigned_pos = {
        row: -1, 
        col: -1
    }

    if (!findUnassignedPos(grid, unassigned_pos)) return true;

    grid.forEach((row, i) => {
        row.forEach((num, j) => {
            if (isSafe(grid, i, j, num)) {    
                if(isGridFull(grid)) {
                    return true;
                } else {
                    if (sudokuCreate(grid)) {
                        return true;
                    }
                }
            }
        })
    })
    return isGridFull(grid);
}

const rand = () => Math.floor(Math.random() * CONSTANT.GRID_SIZE);

const removeCells = (grid, level) => {
    let res = [...grid];
    let attempts = level;
    while (attempts > 0) {
        let row = rand();
        let col = rand();
        while (res[row][col] === 0) {
            row = rand();
            col = rand();
        }
        res[row][col] = CONSTANT.UNASSIGNED;
        attempts--;
    }
    return res;
}

const sudokuGen = (level) => {
    let sudoku = newGrid(CONSTANT.GRID_SIZE);
    let check = sudokuCreate(sudoku);
    if (check) {
        let question = removeCells(sudoku, level);
        return {
            original: sudoku,
            question: question
        }
    }
    return undefined;
}
