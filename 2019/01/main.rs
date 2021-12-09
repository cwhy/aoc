use std::io::BufReader;
use std::io::BufRead;
use std::io;
use std::fs;

fn main() -> io::Result<()> {
    let file_in = fs::File::open("input.txt")?;
    let file_reader = BufReader::new(file_in);
    let sum:i32 = file_reader.lines().map(|line| line.unwrap().parse::<i32>().unwrap()).map(mass2fuel).sum();
    println!("{:?}", sum);
    Ok(())
}

fn mass2fuel(x:i32) -> i32 {
    let fuel_cur_1 = x/3;
    match fuel_cur_1 {
        0 => 0,
        1 => 0,
        2 => 0,
        _ => mass2fuel(fuel_cur_1 - 2) + fuel_cur_1 - 2,
    }
}
