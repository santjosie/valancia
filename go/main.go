package main

import (
	"archive/zip"
	"fmt"
	"io"
	"log"
	"os"
	"path/filepath"
	"strconv"

	"github.com/pdfcpu/pdfcpu/pkg/api"
)

func main() {

	cwd, err := os.Getwd()
	if err != nil {
		log.Fatalf("Error when trying to find the current working directory: %e", err)
	} else {
		fmt.Println("Current working directory is %v", cwd)
	}

	inputPdf := cwd + "\\go\\test.pdf"
	outputDir := cwd + "\\go\\pdfs"
	outputZip := ""

	err = os.MkdirAll(outputDir, os.ModePerm)
	if err != nil {
		log.Fatalf("Failed to create the output directory: %v", err)
	} else {
		fmt.Println("Created output directory %v", outputDir)
	}

	err = splitPdf(inputPdf, outputDir)
	if err != nil {
		log.Fatalf("Error while splitting the pdf: %v", err)
	} else {
		fmt.Println("The PDF file has been split")
	}

	err = zipPdfs(outputDir, outputZip)
	if err != nil {
		log.Fatalf("Error while zipping pdf files: %v", err)
	} else {
		fmt.Println("The split files have been zipped into a zip file")
	}

}

func splitPdf(inputPdf string, outputDir string) error {

	if _, err := os.Stat(inputPdf); os.IsNotExist(err) {
		log.Fatalf("File does not exist: %s", inputPdf)
	}

	ctx, err := api.ReadContextFile(inputPdf)
	if err != nil {
		return fmt.Errorf("Failed to read file %v", inputPdf)
	}

	for i := 1; i <= ctx.PageCount; i++ {
		outputFile := filepath.Join(outputDir, "page"+strconv.Itoa(i)+".pdf")
		err = api.ExtractPagesFile(inputPdf, outputFile, []string{strconv.Itoa((i))}, nil)
		if err != nil {
			return fmt.Errorf("Failed to extract page %p: %e", i, err)
		}
	}

	return nil
}

func zipPdfs(sourceDir, outputZip string) error {
	zipFile, err := os.Create(outputZip)
	if err != nil {
		return fmt.Errorf("Error while trying to create a zip file %e: ", err)
	}

	defer zipFile.Close()

	zipWriter := zip.NewWriter(zipFile)
	defer zipWriter.Close()

	err = filepath.Walk(sourceDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		if info.IsDir() {
			return nil
		}

		relPath, err := filepath.Rel(sourceDir, path)
		if err != nil {
			return err
		}

		zipFile, err := zipWriter.Create(relPath)
		if err != nil {
			return err
		}

		file, err := os.Open(path)
		if err != nil {
			return err
		}
		defer file.Close()

		_, err = io.Copy(zipFile, file)
		if err != nil {
			return err
		}

		return nil
	})

	return nil
}
