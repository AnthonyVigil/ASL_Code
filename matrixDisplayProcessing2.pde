//matrixDisplayProcessing
//Oguz Yetkin 10/14/2019 oyetkin@gmail.com
//written for calibration of the shape sensor for Biomed 2019 Cesme, Turkey
//displays values from a 3x3 matrix obtained from the Arduino,
//MATLAB style
//TODO: accept MATLAB style input

//gridPickProcessing
//Oguz Yetkin 9/25/2018 1:14am
//oyetkin@gmail.com
//use permitted with proper attribution:
//Yetkin, Oguz. Computer Code: gridPickProcessing. September 2018.
//demo code to pick rows and columns graphically


int rows=15;
int cols=15;


//OY 8/6/2018 globals
import processing.serial.*;
int value1; 
int value2;
Serial myPort;


int arena[][];  //this will consist of values between 0-1023 which we will divide by 4
int arenaValueArray[];


//TODO: implement color map
void setup() {
  size(400, 400);
  arena =new int[rows][cols];
  ////seed test squares
  //arena[0][0] = 1020;
  //arena[1][1] = 500;
  //arena[7][7] = true;
  
  arenaValueArray = new int[rows*cols];

  String portName = Serial.list()[0];
  myPort = new Serial(this, portName, 115200);
  myPort.bufferUntil(10);
}

int mapColor(int val) {
  return val/4;
}
void drawGrid(int rows, int cols) {
  int boxw = width/cols;
  int boxh = height/rows;
  int i=0;
  //draw lines
  for (i=0; i<width; i+=boxw) {
    stroke(125, 125, 125);
    line(0, i, width, i);
    //println("0,"+i+"-"+width+","+i);
  }
  for (i=0; i<height; i+=boxh) {

    line(i, 0, i, height);
  }
}

void populateGrid(int[][] arena) {
  int rows = arena.length;
  int cols = arena[0].length; //all rows have the same columns
  //println(rows+","+cols);
  int boxw = width/cols;
  int boxh = height/rows;

  int i, j;
  for (i=0; i<rows; i++) {
    for (j=0; j<cols; j++) {
      //fill(20,20,20); 
      //OY 10/14/2019
      fill(mapColor(arena[i][j]));
      rect(j*boxw, i*boxh, 
        boxw, boxh);
      //if(arena[i][j] == true){
      //  rect(j*boxw,i*boxh,
      //       boxw, boxh);
      //}
    }//end inner for
  }//end outer for
}
void draw() {
  background(255, 255, 255);
  stroke(0);

  populateGrid(arena);
  drawGrid(rows, cols);
  //
}

void mouseClicked() {
  int boxw = width/cols;
  int boxh = height/rows;
  int row = mouseY/boxh;
  int col = mouseX/boxw; //weird but true
  //arena[row][col]=!arena[row][col]; // flip the square
  println("row: "+row+" col: "+col+" val: "+arena[row][col]); //TODO: draw red rect
}

//OY 8/6/2018
void serialEvent(Serial myPort) {
  String valString = myPort.readString(); //needs myPort.bufferUntil(10) in setup()


  if (valString != null) {
    valString= trim(valString);
    println(valString);
    String[] valArray = valString.split(" ");
    try {
      //value1 = int(valArray[0]);
      //value2 = int(valArray[1]);
      
      //parse string array into int array
      for(int i=0;i<rows*cols;i++){
        arenaValueArray[i] = int(valArray[i]);
      }
      
      //reshape arenaValueArray into arena 
      //TODO: handle MATLAB-style strings
      for(int row=0;row<rows;row++){
        for(int col=0;col<cols;col++){
          arena[row][col]=arenaValueArray[row*rows+col];
        }
      }
       

      //arena[0][0] = int(value1);
      //arena[0][1] = int(value2);
      //println("value1: "+value1+" value2: "+value2);
    }

    catch(Exception e) {
      e.printStackTrace();
      println("err");
      value1 = -1;
      value2 = -1;
    }
  }
}
