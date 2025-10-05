using UnityEngine;
using TMPro;
public class FileName : MonoBehaviour
{
    [SerializeField] private ImageLerpController imageLerpController;
    [SerializeField] private string imagename;
    [SerializeField] private TMP_Text textMeshPro;
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {
        imagename = imageLerpController.currentImageName;
        // Split the prefix "bloom_" and the suffix ".png"
        string prefix = "bloom_";
        string suffix = "png";
        string coreName = imagename.Substring(prefix.Length, imagename.Length - prefix.Length - suffix.Length);
        textMeshPro.text = coreName;
    }
}
