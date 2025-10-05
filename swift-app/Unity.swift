//
//  Unity.swift
//  SpaceApps
//
//  Created by Julia Holzbach on 10/4/25.
//

import Foundation
import SwiftUI
/*
struct ContentView: View {
    var body: some View {
        GIFView(gifName: "ModelGif") // Replace "myAnimatedGif" with your GIF's filename
            .frame(width: 200, height: 200) // Adjust size as needed } }
    }
}
*/

struct Unity: View {
    var body: some View {
        ZStack {
            Rectangle().fill(Color.black).ignoresSafeArea()
            VStack {
               // Spacer()
                Link(destination: URL(string: "https://github.com/d-guh/nasa-spaceapps-2025/tree/main/unity-globe")!) {
                    GIFView(name: "ModelGif")
                    //.resizable()
                        .scaledToFit()
                        .ignoresSafeArea()
                        .padding(.top, 100)
                   // Spacer()
                }
            }
          
        }//.background(Color.black)
    }
}
