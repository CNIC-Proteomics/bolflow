# import "setup.wdl" as setup

workflow bolFlow {
  String name
  Array[File] infiles
  File incfile
  # call setup.config {}
  call joinFiles {
    input:
      sampleName=name,
      inFiles=infiles,
      classFile=incfile
  }
  call calcFreq {
    input:
      sampleName=name,
      inFile=joinFiles.outFile
  }
}

# This task calls join_files script.
task joinFiles {
  String sampleName
  Array[File] inFiles
  File classFile
  command {
    python /mnt/projects/metabolomics/bolflow/join_files.py \
      -ii ${sep=" " inFiles} \
      -ic ${classFile} \
      -o ${sampleName}.join.csv
  }
  output {
    File outFile = "${sampleName}.join.csv"
  }
}

# This task calculate the frequency and standard desviation.
task calcFreq {
  String sampleName
  File inFile
  command {
    python /mnt/projects/metabolomics/bolflow/freq-cv.py \
      -i ${inFile} \
      -o ${sampleName}.freq-cv.csv
  }
  output {
    File outFile = "${sampleName}.freq-cv.csv"
  }
}
