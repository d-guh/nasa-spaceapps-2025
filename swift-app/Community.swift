//
//  Community.swift
//  SpaceApps
//
//  Created by Julia Holzbach on 10/4/25.
//

import Foundation
import SwiftUI
import UIKit
import WebKit

struct WebView: UIViewRepresentable {
    let url: URL

    func makeUIView(context: Context) -> WKWebView {
        return WKWebView()
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {
        let request = URLRequest(url: url)
        uiView.load(request)
    }
}

struct Community: View {
    var body: some View {
        WebView(url: URL(string: "https://d-guh.github.io/nasa-spaceapps-2025/bloom_viewer.html")!)
            .edgesIgnoringSafeArea(.all) // Optional: Makes the web view take up the full screen
    }
}
