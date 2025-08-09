"""
Test file for Task 1: Document Loading & Text Extraction
Students can run this to validate their implementation.

Usage: python -m pytest tests/test_task1_document_processing.py -v
"""

import pytest
import io
import sys
from pathlib import Path

# Add parent directory to Python path for imports
sys.path.append(str(Path(__file__).parent.parent))

from backend.services.processor import document_processor

class TestTask1DocumentProcessing:
    
    def test_extract_text_with_pdf(self):
        """Test PDF text extraction functionality"""
        # Create a mock PDF content (this would be real PDF bytes in practice)
        mock_pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj"
        filename = "test_document.pdf"
        
        try:
            result = document_processor._extract_text(mock_pdf_content, filename)
            # Check that method doesn't return the TODO placeholder
            assert result != "TODO: Implement text extraction logic", \
                "❌ TASK 1 INCOMPLETE: You need to implement text extraction logic in _extract_text method"
            print("✅ PDF extraction method implemented")
        except AssertionError as e:
            pytest.fail(f"❌ TASK 1 FAILED: {str(e)}")
        except Exception as e:
            print(f"⚠️  PDF test failed (expected for mock data): {e}")
    
    def test_extract_text_with_txt(self):
        """Test TXT text extraction functionality"""
        test_content = "This is a test document with some sample text content."
        txt_content = test_content.encode('utf-8')
        filename = "test_document.txt"
        
        try:
            result = document_processor._extract_text(txt_content, filename)
            assert result != "TODO: Implement text extraction logic", \
                "❌ TASK 1 INCOMPLETE: You need to implement text extraction logic in _extract_text method"
            assert isinstance(result, str), "❌ Text extraction should return a string"
            print("✅ TXT extraction method implemented")
        except AssertionError as e:
            pytest.fail(f"❌ TASK 1 FAILED: {str(e)}")
    
    def test_extract_text_file_type_handling(self):
        """Test that different file types are handled properly"""
        test_content = b"Sample content"
        
        # Test each supported file type
        file_types = [".pdf", ".docx", ".txt"]
        for ext in file_types:
            filename = f"test{ext}"
            try:
                result = document_processor._extract_text(test_content, filename)
                assert result != "TODO: Implement text extraction logic", \
                    f"❌ TASK 1 INCOMPLETE: Text extraction not implemented for {ext} files"
                print(f"✅ {ext} file type handling implemented")
            except AssertionError:
                raise
            except Exception as e:
                print(f"⚠️  {ext} test failed (may be expected for mock data): {e}")
    
    def test_chunking_implementation(self):
        """Test that text chunking is implemented"""
        # Test with sample text
        sample_text = "This is a test document. " * 100  # Long enough to require chunking
        
        try:
            # This would normally be called from process_document, but we'll test the chunking part
            chunks = document_processor.text_splitter.split_text(sample_text)
            
            # Check if chunking produces reasonable results
            assert len(chunks) > 0, "❌ TASK 1 FAILED: Chunking should produce at least one chunk"
            assert all(isinstance(chunk, str) for chunk in chunks), "❌ TASK 1 FAILED: All chunks should be strings"
            assert chunks[0] != "TODO: Implement chunking logic", \
                "❌ TASK 1 INCOMPLETE: You need to implement chunking logic in process_document method"
            
            print(f"✅ Text chunking working - produced {len(chunks)} chunks")
            
        except Exception as e:
            pytest.fail(f"❌ TASK 1 FAILED: Chunking error - {str(e)}")
    
    def test_file_validation(self):
        """Test file validation works correctly"""
        processor = document_processor
        
        # Test valid files
        valid_result, msg = processor.validate_file("document.pdf", 1024 * 1024)  # 1MB
        assert valid_result, f"❌ Valid PDF should pass validation: {msg}"
        
        # Test invalid file type
        invalid_result, msg = processor.validate_file("document.exe", 1024)
        assert not invalid_result, "❌ Invalid file type should fail validation"
        
        print("✅ File validation working correctly")

def run_task1_tests():
    """Helper function to run Task 1 tests with nice output"""
    print("🧪 TESTING TASK 1: Document Loading & Text Extraction")
    print("=" * 60)
    
    test_class = TestTask1DocumentProcessing()
    
    tests = [
        ("PDF text extraction", test_class.test_extract_text_with_pdf),
        ("TXT text extraction", test_class.test_extract_text_with_txt), 
        ("File type handling", test_class.test_extract_text_file_type_handling),
        ("Text chunking", test_class.test_chunking_implementation),
        ("File validation", test_class.test_file_validation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            print(f"\n📋 Testing {test_name}...")
            test_func()
            passed += 1
        except Exception as e:
            print(f"❌ {test_name} FAILED: {str(e)}")
    
    print(f"\n📊 TASK 1 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 TASK 1 COMPLETE! Great job implementing document processing!")
    else:
        print("⚠️  Some tests failed. Check the error messages above for guidance.")
        print("\n💡 DEBUGGING TIPS:")
        print("- Make sure you uncommented the template code in processor.py")
        print("- Check that your text extraction logic handles all file types")
        print("- Verify that chunking logic is properly implemented")

if __name__ == "__main__":
    run_task1_tests()